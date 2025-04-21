from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QPushButton, QVBoxLayout


class Transport(QWidget):
    def __init__(self):
        super().__init__()
        self.group_box = QGroupBox(f"Transport")
        self.btn_play = QPushButton("Play")
        self.btn_stop = QPushButton("Stop")

        self.initialise_components()

    def initialise_components(self):
        layout = QGridLayout()
        layout.addWidget(self.btn_play, 0, 0)
        layout.addWidget(self.btn_stop, 1, 0)
        self.configure_buttons()

        self.group_box.setLayout(layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

    def configure_buttons(self):
        for btn in [self.btn_play, self.btn_stop]:
            btn.setFixedSize(100, 100)


