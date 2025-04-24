import numpy as np

from sound_engine.synth_waves.SynthWaveform import SynthWaveform


class PulseWave(SynthWaveform):
    def __init__(self, frequency=440, duty_cycle=0.5, volume=0.5, duration=1.0, samplerate=44100):
        self.__duty_cycle = duty_cycle
        t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
        wave = volume * np.where(t * frequency - np.floor(t * frequency) < self.__duty_cycle, 1, -1)
        super().__init__(wave, frequency, volume, duration, samplerate)

    @property
    def duty_cycle(self):
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.__duty_cycle = value
