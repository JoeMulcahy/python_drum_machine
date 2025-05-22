from scipy.signal import sosfiltfilt

from sound_engine.audio_filters.equalisation_worker import EQWorker


class SimpleEqualisation:
    """Simple synchronous EQ implementation for most use cases"""

    @staticmethod
    def apply_eq(data, gain_db, frequency, q=0.707, sample_rate=44100, eq_type='low_shelf'):
        """Apply EQ directly without threading"""
        worker = EQWorker()

        # Calculate coefficients
        sos = worker._calculate_biquad_sos(gain_db, frequency, q, sample_rate, eq_type)

        # Apply filter
        return sosfiltfilt(sos, data)