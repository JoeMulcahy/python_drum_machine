from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from Channel import Channel
from DrumMachine import DrumMachine
from sequencer_module.SequencerModule import SequencerModule
from transport_module.Transport import Transport


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        app_layout = QVBoxLayout()
        app_layout.addWidget(DrumMachine())

        widget = QWidget()
        widget.setLayout(app_layout)

        self.setCentralWidget(widget)
