from PyQt6.QtCore import pyqtSignal, QObject


class DrumMachineSignals(QObject):
    def __init__(self, *signal_types):
        super().__init__()
        self.__pulse_signal = pyqtSignal(*signal_types)

    @property
    def pulse_signal(self):
        return self.__pulse_signal




