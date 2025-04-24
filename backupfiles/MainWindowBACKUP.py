from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from Drum_Machine_Channel import Channel
from sequencer_module.SequencerModule import SequencerModule
from transport_module.Transport import Transport


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        app_layout = QGridLayout()

        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        layout2 = QGridLayout()
        layout2.setSpacing(15)
        layout2.setContentsMargins(10, 10, 10, 10)

        layout.addWidget(Channel(1), 0, 0)
        layout.addWidget(Channel(2), 0, 1)
        layout.addWidget(Channel(3), 0, 2)
        layout.addWidget(Channel(4), 0, 3)
        layout.addWidget(Channel(5), 0, 4)
        layout.addWidget(Channel(6), 0, 5)
        layout.addWidget(Channel(7), 0, 6)
        layout.addWidget(Channel(8), 0, 7)

        layout2.addWidget(Transport(), 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout2.addWidget(SequencerModule(16), 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout2.setColumnStretch(0, 2)
        layout2.setColumnStretch(1, 5)

        app_layout.addLayout(layout, 0, 0)
        app_layout.addLayout(layout2, 1, 0)

        widget = QWidget()
        widget.setLayout(app_layout)

        self.setCentralWidget(widget)
