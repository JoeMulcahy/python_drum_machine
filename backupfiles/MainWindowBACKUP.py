from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from DrumMachineChannel import DrumMachineChannel
from sequencer_module.sequencer_module import SequencerModule
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

        layout.addWidget(DrumMachineChannel(1), 0, 0)
        layout.addWidget(DrumMachineChannel(2), 0, 1)
        layout.addWidget(DrumMachineChannel(3), 0, 2)
        layout.addWidget(DrumMachineChannel(4), 0, 3)
        layout.addWidget(DrumMachineChannel(5), 0, 4)
        layout.addWidget(DrumMachineChannel(6), 0, 5)
        layout.addWidget(DrumMachineChannel(7), 0, 6)
        layout.addWidget(DrumMachineChannel(8), 0, 7)

        layout2.addWidget(Transport(), 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout2.addWidget(SequencerModule(16), 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout2.setColumnStretch(0, 2)
        layout2.setColumnStretch(1, 5)

        app_layout.addLayout(layout, 0, 0)
        app_layout.addLayout(layout2, 1, 0)

        widget = QWidget()
        widget.setLayout(app_layout)

        self.setCentralWidget(widget)
