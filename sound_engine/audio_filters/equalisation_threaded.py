import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from scipy.signal import sosfiltfilt

from sound_engine.audio_filters.equalisation_worker import EQWorker


class Equalisation(QObject):
    filtered_data = pyqtSignal(np.ndarray)
    error_occurred = pyqtSignal(str)

    def __init__(self, use_threading=False):
        super().__init__()
        self._use_threading = use_threading
        self._thread = None
        self._worker = None

    def apply_eq(self, data, gain_db, frequency, q=0.707, sample_rate=44100, eq_type='low_shelf'):
        """Apply equalization to audio data"""
        if self._use_threading:
            self._apply_eq_threaded(data, gain_db, frequency, q, sample_rate, eq_type)
        else:
            # Direct processing on main thread
            try:
                worker = EQWorker()
                worker.processed_signal.connect(self.filtered_data.emit)
                worker.error_signal.connect(self.error_occurred.emit)
                worker.process_eq(data, gain_db, frequency, q, sample_rate, eq_type)
            except Exception as e:
                self.error_occurred.emit(str(e))

    def _apply_eq_threaded(self, data, gain_db, frequency, q, sample_rate, eq_type):
        """Apply EQ using background thread"""
        # Clean up previous operation
        self._cleanup_thread()

        # Create new thread and worker
        self._thread = QThread()
        self._worker = EQWorker()
        self._worker.moveToThread(self._thread)

        # Connect signals
        self._worker.processed_signal.connect(self._on_processed)
        self._worker.error_signal.connect(self._on_error)
        self._thread.started.connect(
            lambda: self._worker.process_eq(data, gain_db, frequency, q, sample_rate, eq_type)
        )

        # Start processing
        self._thread.start()

    def _on_processed(self, processed_data):
        """Handle processed audio data"""
        self.filtered_data.emit(processed_data)
        self._cleanup_thread()

    def _on_error(self, error_message):
        """Handle processing errors"""
        self.error_occurred.emit(error_message)
        self._cleanup_thread()

    def _cleanup_thread(self):
        """Clean up thread resources"""
        if self._thread is not None:
            if self._worker:
                self._worker.stop()
            self._thread.quit()
            self._thread.wait(5000)  # Wait up to 5 seconds
            if self._thread.isRunning():
                self._thread.terminate()
                self._thread.wait()
            self._thread.deleteLater()
            self._thread = None
            self._worker = None

    def stop_processing(self):
        """Stop current processing operation"""
        if self._worker:
            self._worker.stop()

    def __del__(self):
        """Cleanup when object is destroyed"""
        self._cleanup_thread()


