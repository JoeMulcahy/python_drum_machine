from app_enums.wave_form_enum import WaveForm
from sound_engine.SynthVoice import SynthVoice


class Metronome:
    def __init__(self, tempo=120, beats_per_bar=4, meter=4):
        self.__tempo = tempo
        self.__beats_per_bar = beats_per_bar
        self.__meter = meter

        self.__metronome_voice_hi = SynthVoice(WaveForm.SQUARE, 880, 0.05, 0.5, 44100)
        self.__metronome_voice_lo = SynthVoice(WaveForm.SQUARE, 440, 0.05, 0.5, 44100)
        self.__metronome_voice = self.__metronome_voice_hi

    def metronome_tick_voice(self, count):
        if count % self.beats_per_bar == 0:
            self.__metronome_voice = self.__metronome_voice_hi
        else:
            self.__metronome_voice = self.__metronome_voice_lo

        return self.__metronome_voice

    @property
    def tempo(self):
        return self.__tempo

    @tempo.setter
    def tempo(self, value):
        self.__tempo = value

    @property
    def beats_per_bar(self):
        return self.__beats_per_bar

    @beats_per_bar.setter
    def beats_per_bar(self, value):
        self.__beats_per_bar = value

    @property
    def meter(self):
        return self.__meter

    @meter.setter
    def meter(self, value):
        self.__meter = value

    @property
    def metronome_voice(self):
        return self.__metronome_voice

    @metronome_voice.setter
    def metronome_voice(self, value):
        self.__metronome_voice = value
