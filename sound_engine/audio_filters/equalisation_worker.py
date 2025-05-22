import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMutex, QMutexLocker
from scipy.signal import sosfiltfilt
import logging


class EQWorker(QObject):
    processed_signal = pyqtSignal(np.ndarray)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._should_stop = False
        self._mutex = QMutex()

    def stop(self):
        with QMutexLocker(self._mutex):
            self._should_stop = True

    def process_eq(self, data, gain_db, frequency, q=0.707, sample_rate=44100, eq_type='low_shelf'):
        try:
            # Input validation
            if not isinstance(data, np.ndarray):
                raise ValueError("Data must be a numpy array")
            if len(data) == 0:
                raise ValueError("Data array is empty")
            if sample_rate <= 0:
                raise ValueError("Sample rate must be positive")
            if frequency <= 0 or frequency >= sample_rate / 2:
                raise ValueError("Frequency must be between 0 and Nyquist frequency")

            # Check if we should stop
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            # Calculate filter coefficients
            sos = self._calculate_biquad_sos(gain_db, frequency, q, sample_rate, eq_type)

            # Check if we should stop before processing
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            # Apply filter
            processed = sosfiltfilt(sos, data)

            # Check if we should stop before emitting
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            self.processed_signal.emit(processed)

        except Exception as e:
            logging.error(f"EQ processing error: {str(e)}")
            self.error_signal.emit(str(e))

    def _calculate_biquad_sos(self, gain_db, frequency, q, sample_rate, eq_type):
        """Calculate second-order section coefficients for biquad filter"""
        amplitude = 10 ** (gain_db / 40)
        w0 = 2 * np.pi * frequency / sample_rate
        cos_w0 = np.cos(w0)
        sin_w0 = np.sin(w0)

        if eq_type == 'parametric':
            alpha = sin_w0 / (2 * q)
        else:
            # For shelf filters, use a different alpha calculation
            S = 1  # Shelf slope parameter (could be made configurable)
            alpha = sin_w0 / 2 * np.sqrt((amplitude + 1 / amplitude) * (1 / S - 1) + 2)

        if eq_type == 'low_shelf':
            b0 = amplitude * ((amplitude + 1) - (amplitude - 1) * cos_w0 + 2 * np.sqrt(amplitude) * alpha)
            b1 = 2 * amplitude * ((amplitude - 1) - (amplitude + 1) * cos_w0)
            b2 = amplitude * ((amplitude + 1) - (amplitude - 1) * cos_w0 - 2 * np.sqrt(amplitude) * alpha)
            a0 = (amplitude + 1) + (amplitude - 1) * cos_w0 + 2 * np.sqrt(amplitude) * alpha
            a1 = -2 * ((amplitude - 1) + (amplitude + 1) * cos_w0)
            a2 = (amplitude + 1) + (amplitude - 1) * cos_w0 - 2 * np.sqrt(amplitude) * alpha

        elif eq_type == 'high_shelf':
            b0 = amplitude * ((amplitude + 1) + (amplitude - 1) * cos_w0 + 2 * np.sqrt(amplitude) * alpha)
            b1 = -2 * amplitude * ((amplitude - 1) + (amplitude + 1) * cos_w0)
            b2 = amplitude * ((amplitude + 1) + (amplitude - 1) * cos_w0 - 2 * np.sqrt(amplitude) * alpha)
            a0 = (amplitude + 1) - (amplitude - 1) * cos_w0 + 2 * np.sqrt(amplitude) * alpha
            a1 = 2 * ((amplitude - 1) - (amplitude + 1) * cos_w0)
            a2 = (amplitude + 1) - (amplitude - 1) * cos_w0 - 2 * np.sqrt(amplitude) * alpha

        elif eq_type == 'parametric':
            b0 = 1 + alpha * amplitude
            b1 = -2 * cos_w0
            b2 = 1 - alpha * amplitude
            a0 = 1 + alpha / amplitude
            a1 = -2 * cos_w0
            a2 = 1 - alpha / amplitude

        else:
            raise ValueError(f"Invalid EQ type: {eq_type}")

        # Normalize coefficients
        b = np.array([b0, b1, b2]) / a0
        a = np.array([1.0, a1 / a0, a2 / a0])

        # Return as second-order section
        return np.array([[b[0], b[1], b[2], a[0], a[1], a[2]]])