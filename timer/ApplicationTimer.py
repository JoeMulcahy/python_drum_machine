import threading
import time


class ApplicationTimer(threading.Thread):
    def __init__(self, tempo, beats_per_bar, meter):
        super().__init__()
        self.stop_event = None
        self.thread = None
        self.__counter = 0
        self.__is_counting = False
        self.__tempo = tempo
        self.__beats_per_bar = beats_per_bar
        self.__meter = meter
        self.__interval = 60 / self.__tempo * (self.__beats_per_bar / self.__meter)

    def app_counter(self):
        while not self.stop_event.is_set():
            if self.__is_counting:
                print(f"tick - {self.__counter}")
                time.sleep(self.__interval)
                self.__counter += 1
            else:
                time.sleep(0.1)

    def start_counter(self):
        self.stop_event = threading.Event()
        self.reset_counter()
        self.__is_counting = True
        self.thread = threading.Thread(target=self.app_counter)
        self.thread.start()

    def stop_counter(self):
        self.__is_counting = False
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()  # waits for thread to fully stop
        self.reset_counter()

    def reset_counter(self):
        self.__counter = 0

    @property
    def counter(self):
        return self.__counter

    @property
    def tempo(self):
        return self.__tempo

    @property
    def beats_per_bar(self):
        return self.__beats_per_bar

    @property
    def meter(self):
        return self.__meter

    @counter.setter
    def counter(self, value):
        self.__counter = value

    @tempo.setter
    def tempo(self, value):
        self.__tempo = value

    @beats_per_bar.setter
    def beats_per_bar(self, value):
        self.__beats_per_bar = value

    @meter.setter
    def meter(self, value):
        self.__meter = value

    def set_timing_resolution(self, bpb, meter):
        self.__beats_per_bar = bpb
        self.__meter = meter
        self.calculate_interval()

    def set_tempo(self, value):
        self.__tempo = value
        self.calculate_interval()

    def calculate_interval(self):
        self.__interval = 60 / self.__tempo / (self.__beats_per_bar / self.__meter)
