from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from app_enums.wave_form_enum import WaveForm
from sound_engine.synth_sample import SynthVoice


class MetronomeWorker(QObject):
    pulse_signal = pyqtSignal(int)

    def __init__(self, tempo, bpb, beat_type):
        super().__init__()
        self.thirty_second_note_counter = 0
        self.pulse_counter = 0
        self.tempo = tempo
        self.bpb = bpb
        self.beat_type = beat_type
        self.counter = 0
        self.is_running = True

    @pyqtSlot()
    def run(self):
        self.pulse_counter = 0  # Counter for the actual beats
        while self.is_running:
            self.pulse_signal.emit(self.pulse_counter)
            interval_per_beat = int((60 / self.worker_tempo) * 1000 / (self.beat_type / 4))
            QThread.msleep(interval_per_beat)
            self.pulse_counter += 1

    def stop(self):
        self.is_running = False
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        self.thread = None

    @property
    def worker_tempo(self):
        return self.tempo

    @worker_tempo.setter
    def worker_tempo(self, val):
        self.tempo = val

    @property
    def worker_bpb(self):
        return self.bpb

    @worker_bpb.setter
    def worker_bpb(self, val):
        self.bpb = val

    @property
    def worker_beat_type(self):
        return self.beat_type

    @worker_beat_type.setter
    def worker_beat_type(self, val):
        self.beat_type = val


class Metronome(QObject):
    metronome_voice_signal = pyqtSignal(SynthVoice)

    def __init__(self, tempo=120, beats_per_bar=4, beat_type=4):
        super().__init__()
        self.metro_thread = None
        self.metro_worker = MetronomeWorker(tempo, beats_per_bar, 4)
        self.counter = 0

        self.__tempo = tempo
        self.__beats_per_bar = beats_per_bar
        self.__beat_type = beat_type

        self.__metronome_voice_accented = SynthVoice(WaveForm.SQUARE, 880, 0.05, 0.5, 44100)
        self.__metronome_voice_sixteenth = SynthVoice(WaveForm.SIN, 440, 0.05, 0.5, 44100)
        self.__metronome_voice_eighth = SynthVoice(WaveForm.SAWTOOTH, 440, 0.05, 0.5, 44100)
        self.__metronome_voice_fourth = SynthVoice(WaveForm.SQUARE, 440, 0.05, 0.5, 44100)
        self.__metronome_voice = self.__metronome_voice_accented

    def metronome_tick_voice(self, beat_counter):
        # Determine which beat we’re on in the current bar
        beat_index = (beat_counter) % self.__beats_per_bar

        # Get accent pattern for current time signature
        pattern = self.get_accent_pattern(self.__beats_per_bar, self.__beat_type)

        if pattern[beat_index] == "a":  # accented
            self.__metronome_voice = self.__metronome_voice_accented
        elif pattern[beat_index] == "i":  # intermediate
            self.__metronome_voice = self.__metronome_voice_eighth
        elif pattern[beat_index] == "s":
            self.__metronome_voice = self.__metronome_voice_sixteenth
        else:  # downbeat
            self.__metronome_voice = self.__metronome_voice_fourth

        self.metronome_voice_signal.emit(self.__metronome_voice)

    def get_accent_pattern(self, beats_per_bar, beat_type):
        # print(f"{beats_per_bar}/{beat_type}")
        # Patterns are based on common practice accent groupings
        if beat_type == 4:
            if beats_per_bar == 2:
                return ["a", "d"]
            elif beats_per_bar == 3:
                return ["a", "d", "d"]
            elif beats_per_bar == 4:
                return ["a", "d", "d", "d"]
            elif beats_per_bar == 5:
                return ["a", "d", "d", "d", "d"]
            elif beats_per_bar == 6:
                return ["a", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 7:
                return ["a", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 8:
                return ["a", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 9:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 10:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 11:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 12:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 13:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 14:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 15:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
            elif beats_per_bar == 16:
                return ["a", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]

        elif beat_type == 8:
            if beats_per_bar == 2:
                return ["a", "d"]
            elif beats_per_bar == 3:
                return ["a", "i", "d"]
            elif beats_per_bar == 4:
                return ["a", "i", "d", "i"]
            elif beats_per_bar == 5:
                return ["a", "d", "d", "i", "d"]
            elif beats_per_bar == 6:
                return ["a", "i", "d", "a", "i", "d"]
            elif beats_per_bar == 7:
                return ["a", "d", "i", "d", "i", "i", "d"]
            elif beats_per_bar == 8:
                return ["a", "i", "d", "i", "a", "i", "d", "i"]
            elif beats_per_bar == 9:
                return ["a", "i", "d", "a", "i", "d", "a", "i", "d"]
            elif beats_per_bar == 10:
                return ["a", "i", "d", "i", "a", "i", "d", "i", "a", "d"]
            elif beats_per_bar == 11:
                return ["a", "i", "d", "i", "a", "i", "d", "i", "a", "i", "d"]
            elif beats_per_bar == 12:
                return ["a", "i", "d", "i"] * 3
            elif beats_per_bar == 13:
                return ["a", "i", "d", "i", "a", "i", "d", "i", "a", "i", "d", "i", "d"]
            elif beats_per_bar == 14:
                return ["a", "i", "d", "i", "a", "i", "d", "i", "a", "i", "d", "i", "a", "d"]
            elif beats_per_bar == 15:
                return ["a", "i", "d", "i", "a", "i", "d", "i", "a", "i", "d", "i", "a", "i", "d"]
            elif beats_per_bar == 16:
                return ["a", "i", "d", "i"] * 4

        elif beat_type == 16:
            if beats_per_bar == 2:
                return ["a", "d"]
            elif beats_per_bar == 3:
                return ["a", "s", "d"]  # Assuming "s" for sixteenth note subdivision
            elif beats_per_bar == 4:
                return ["a", "s", "i", "d"]
            elif beats_per_bar == 5:
                return ["a", "s", "s", "i", "d"]
            elif beats_per_bar == 6:
                return ["a", "s", "i", "s", "i", "d"]
            elif beats_per_bar == 7:
                return ["a", "s", "s", "i", "s", "s", "d"]
            elif beats_per_bar == 8:
                return ["a", "s", "i", "s", "i", "s", "i", "d"]
            elif beats_per_bar == 9:
                return ["a", "s", "s", "i", "s", "s", "i", "s", "d"]
            elif beats_per_bar == 10:
                return ["a", "s", "i", "s", "i", "s", "i", "s", "i", "d"]
            elif beats_per_bar == 11:
                return ["a", "s", "s", "i", "s", "s", "i", "s", "s", "i", "d"]
            elif beats_per_bar == 12:
                return ["a", "s", "i", "s", "i", "s", "i", "s", "i", "s", "i", "d"]
            elif beats_per_bar == 13:
                return ["a", "s", "s", "i", "s", "s", "i", "s", "s", "i", "s", "s", "d"]
            elif beats_per_bar == 14:
                return ["a", "s", "i", "s", "i", "s", "i", "s", "i", "s", "i", "s", "i", "d"]
            elif beats_per_bar == 15:
                return ["a", "s", "s", "i", "s", "s", "i", "s", "s", "i", "s", "s", "i", "s", "d"]
            elif beats_per_bar == 16:
                return ["a", "s", "i", "s", "i", "s", "i", "s", "i", "s", "i", "s", "i", "s", "i", "d"]
        elif beat_type == 2:  # for 2/2 or cut time
            return ["a", "d"]
        elif beat_type == 1:
            return ["a"]

    def start_metronome(self):
        self.metro_worker.is_running = True
        self.metro_thread = QThread()
        self.metro_worker = MetronomeWorker(self.__tempo, self.__beats_per_bar, self.__beat_type)
        self.metro_worker.moveToThread(self.metro_thread)
        self.metro_thread.started.connect(self.metro_worker.run)
        self.metro_worker.pulse_signal.connect(self.metronome_tick_voice)
        self.metro_thread.start()

    def stop_metronome(self):
        self.metro_worker.is_running = False
        self.metro_worker.pulse_signal.disconnect()
        self.metro_thread.quit()
        self.metro_thread.wait()
        self.metro_thread.deleteLater()
        self.metro_thread = None

    def update_pulse(self, value):
        self.counter = value

    @property
    def tempo(self):
        return self.__tempo

    @tempo.setter
    def tempo(self, value):
        self.__tempo = value
        self.metro_worker.worker_tempo = value

    @property
    def beats_per_bar(self):
        return self.__beats_per_bar

    @beats_per_bar.setter
    def beats_per_bar(self, value):
        self.__beats_per_bar = value
        self.metro_worker.worker_bpb = value

    @property
    def beat_type(self):
        return self.__beat_type

    @beat_type.setter
    def beat_type(self, value):
        self.__beat_type = value
        self.metro_worker.worker_beat_type = value

    @property
    def metronome_voice(self):
        return self.__metronome_voice

    @metronome_voice.setter
    def metronome_voice(self, value):
        self.__metronome_voice = value
