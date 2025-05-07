from PyQt6.QtCore import pyqtSignal, QObject


class DrumMachineSignals(QObject):
    pulse_signal = pyqtSignal(int)  # Or whatever data you want to send
