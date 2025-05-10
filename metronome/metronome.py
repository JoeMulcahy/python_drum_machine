from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from app_enums.wave_form_enum import WaveForm
from sound_engine.SynthVoice import SynthVoice


class MetronomeWorker(QObject):
    count_signal = pyqtSignal(int)

    def __init__(self, tempo, bpb, beat_type):
        super().__init__()
        self.thirty_second_note_counter = 0
        self.beat_counter = 0
        self.tempo = tempo
        self.bpb = bpb
        self.beat_type = beat_type
        self.counter = 0
        self.is_running = True
        self.thread = None

    @pyqtSlot()
    def run(self):
        self.thread = QThread()
        self.beat_counter = 0  # Counter for the actual beats
        self.thread.start()
        while self.is_running:
            # Calculate the interval for one BEAT (based on beat_type) in milliseconds
            interval_per_beat = int((60 / self.worker_tempo) * 1000)

            # Calculate the interval for one 32nd note (still needed for timing)
            interval_32nd = interval_per_beat / 32

            # Instead of incrementing every 32nd note, sleep for the 32nd note interval
            self.thread.msleep(int(interval_32nd))

            # Keep track of the number of 32nd notes passed within the current beat
            self.thirty_second_note_counter += 1

            # When we've reached the end of a beat (32 x beat_division), emit a beat signal
            beat_division = 32 / self.beat_type * 8  # Assuming beat_type refers to the denominator (e.g., 4 for quarter note)

            if self.thirty_second_note_counter >= beat_division:
                self.beat_counter += 1
                self.count_signal.emit(self.beat_counter)  # Emit the beat number
                self.thirty_second_note_counter = 0  # Reset for the next beat

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
    def worker_meter(self):
        return self.beat_type

    @worker_meter.setter
    def worker_meter(self, val):
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

        self.__metronome_voice_hi = SynthVoice(WaveForm.SQUARE, 880, 0.05, 0.5, 44100)
        self.__metronome_voice_lo = SynthVoice(WaveForm.SQUARE, 440, 0.05, 0.5, 44100)
        self.__metronome_voice = self.__metronome_voice_hi

    def metronome_tick_voice(self, beat_counter):  # Renamed counter for clarity
        print(f'metronome_tick_voice (beat): {beat_counter}')

        if (beat_counter - 1) % self.beats_per_bar == 0:
            self.__metronome_voice = self.__metronome_voice_hi  # Accented beat (on the first beat of the bar)
        else:
            self.__metronome_voice = self.__metronome_voice_lo  # Regular beat

        self.metronome_voice_signal.emit(self.__metronome_voice)

    def start_metronome(self):
        self.metro_worker.is_running = True
        self.metro_thread = QThread()
        self.metro_worker = MetronomeWorker(self.__tempo, self.__beats_per_bar, self.__beat_type)
        self.metro_worker.moveToThread(self.metro_thread)
        self.metro_thread.started.connect(self.metro_worker.run)
        self.metro_worker.count_signal.connect(self.metronome_tick_voice)
        self.metro_thread.start()

    def stop_metronome(self):
        self.metro_worker.is_running = False
        self.metro_worker.count_signal.disconnect()
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
        self.metro_worker.worker_meter = value

    @property
    def metronome_voice(self):
        return self.__metronome_voice

    @metronome_voice.setter
    def metronome_voice(self, value):
        self.__metronome_voice = value
