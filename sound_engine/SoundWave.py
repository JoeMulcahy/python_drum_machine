######################################################################################
##  Basic Sound Wave Generation
##      -Sin
##      -Square
##      -Triangle
##      -Noise ---(TODO)---
######################################################################################
import numpy as np

from app_enums.SoundType import SoundType
from sound_engine.SoundPlayer import SoundPlayer


class SoundWave(SoundPlayer):
    def __init__(self, name, frequency, duration, volume, sample_rate, wave_form):
        self.frequency = frequency
        self.duration = duration
        self.volume = volume
        self.sample_rate = sample_rate
        self.wave_form = wave_form
        self.sound = self.get_waveform()
        self.sound = self.sound.astype(np.float32) / 32768.0
        super().__init__(name, SoundType.SOUND_WAVE, self.sound, sample_rate)

    def get_waveform(self):
        # Placeholder: to be overridden by subclasses
        return np.zeros(int(self.sample_rate * self.duration))


class SinWave(SoundWave):
    def __init__(self, name, frequency, duration, volume, sample_rate):
        self.frequency = frequency
        self.duration = duration
        self.volume = volume
        self.sample_rate = sample_rate
        super().__init__(name, frequency, duration, volume, sample_rate, wave_form="sine")

    def get_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        return self.volume * np.sin(2 * np.pi * self.frequency * t)


class SquareWave(SoundWave):
    def __init__(self, name, frequency, duration, volume, sample_rate):
        self.frequency = frequency
        self.duration = duration
        self.sample_rate = sample_rate
        super().__init__(name, frequency, duration, volume, sample_rate, wave_form="square")

    def get_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        return self.volume * np.sign(np.sin(2 * np.pi * self.frequency * t))


class TriangleWave(SoundWave):
    def __init__(self, name, frequency, duration, volume, sample_rate):
        self.frequency = frequency
        self.duration = duration
        self.sample_rate = sample_rate
        super().__init__(name, frequency, duration, volume, sample_rate, wave_form="triangle")

    def get_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        return self.volume * (2 * np.abs(2 * (t * self.frequency - np.floor(t * self.frequency + 0.5))) - 1)
