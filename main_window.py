# main_window.py

from PyQt6.QtWidgets import *

from drum_machine import DrumMachine
from signals import DrumMachineSignals


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyBeats")
        self.central_widget = QWidget()
        self.app_layout = QGridLayout()
        self.drum_machine = DrumMachine()
        self.app_layout.addWidget(self.drum_machine)
        self.central_widget.setLayout(self.app_layout)
        # self.setFixedSize(1920, 1080)
        self.setCentralWidget(self.central_widget)

        # Connect the signal from DrumMachine to the slot in MainWindow
        self.drum_machine.restart_requested_signal.connect(self._reinitialize_drum_machine)

    def _reinitialize_drum_machine(self):
        # Remove the old drum machine widget
        self.app_layout.removeWidget(self.drum_machine)
        self.drum_machine.deleteLater()
        self.drum_machine = None

        # Create a new instance of DrumMachine
        self.drum_machine = DrumMachine()

        # Add the new drum machine widget to the layout
        self.app_layout.addWidget(self.drum_machine)

        # Re-establish the signal connection for the new instance
        self.drum_machine.restart_requested_signal.connect(self._reinitialize_drum_machine)

        # Force a layout update
        self.central_widget.setLayout(self.app_layout)