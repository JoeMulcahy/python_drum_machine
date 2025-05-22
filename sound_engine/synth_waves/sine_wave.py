import numpy as np

from sound_engine.synth_waves.base_waveform import BaseWaveform


class SinWave(BaseWaveform):
    def __init__(self, frequency, volume, duration, samplerate=44100):
        t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
        wave = volume * np.sin(2 * np.pi * frequency * t)
        super().__init__(wave, frequency, volume, duration, samplerate)
