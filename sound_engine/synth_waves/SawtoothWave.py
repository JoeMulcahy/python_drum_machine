import numpy as np

from sound_engine.synth_waves.SynthWaveform import SynthWaveform


class SawtoothWave(SynthWaveform):
    def __init__(self, frequency=440, volume=0.5, duration=1.0, samplerate=44100):
        t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
        wave = volume * (2 * (t * frequency - np.floor(t * frequency + 0.5)) - 1)
        super().__init__(wave, frequency, volume, duration, samplerate)
