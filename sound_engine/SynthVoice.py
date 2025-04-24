from sound_engine.Voice import Voice
from sound_engine.synth_waves import NoiseWave, SinWave, SawtoothWave, SquareWave, PulseWave, TriangleWave
from app_enums.WaveForm import WaveForm


class SynthVoice(Voice):
    def __init__(self, waveform, samplerate):
        self.__frequency = 440
        self.__duration = 1.0
        self.__volume = 0.5
        self.__samplerate = samplerate
        self.__data = self.__get_synth_waveform(waveform)
        self.__samplerate = samplerate
        super().__init__(self.__data, self.__samplerate)

    def __get_synth_waveform(self, wave_type):
        if wave_type == WaveForm.SIN:
            return SinWave(frequency=self.__frequency, duration=self.__duration, volume=self.__volume, samplerate=self.__samplerate)
        elif wave_type == WaveForm.SQUARE:
            return SquareWave(frequency=self.__frequency, duration=self.__duration, volume=self.__volume, samplerate=self.__samplerate)
        elif wave_type == WaveForm.TRIANGLE:
            return TriangleWave(frequency=self.__frequency, duration=self.__duration, volume=self.__volume, samplerate=self.__samplerate)
        elif wave_type == WaveForm.SAWTOOTH:
            return SawtoothWave(frequency=self.__frequency, duration=self.__duration, volume=self.__volume, samplerate=self.__samplerate)
        elif wave_type == WaveForm.PULSE:
            return PulseWave(frequency=self.__frequency, duty_cycle=0.5, duration=self.__duration, volume=self.__volume, samplerate=self.__samplerate)
        else:
            return NoiseWave(duration=self.__duration, volume=self.__volume, samplerate=self.__samplerate)


