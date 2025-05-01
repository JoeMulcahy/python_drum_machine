from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from drum_machine_channel import DrumMachineChannel
from drum_machine import DrumMachine
from sequencer_module.sequencer_module import SequencerModule
from transport.transport import Transport


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Widgets App")
        app_layout = QGridLayout()
        app_layout.addWidget(DrumMachine())
        widget = QWidget()
        widget.setLayout(app_layout)
        self.setCentralWidget(widget)
