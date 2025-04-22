from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QSpinBox, QLabel, QCheckBox


class Transport(QWidget):
    def __init__(self):
        super().__init__()
        self.__is_playing = False

        self.__group_box = QGroupBox(f"Transport")

        self.__btn_play = QPushButton("Play")
        self.__btn_stop = QPushButton("Stop")

        self.__tempo_spin_box = QSpinBox()
        self.__tempo_spin_box.setRange(1, 300)
        self.__tempo_spin_box.setValue(120)
        self.__tempo_spin_box.setFixedSize(100, 100)
        self.__tempo_spin_box.setStyleSheet("""
            QSpinBox {
                font-size: 24px;       /* Resize text */
                color: #ff5733;        /* Change text color */
            }
        """)
        self.__tempo_label = QLabel("Tempo")

        self.__metronome_checkbox = QCheckBox()
        self.__metronome_checkbox.setChecked(False)
        self.__metronome_label = QLabel("Metronome on/off")

        self.initialise_components()

    def initialise_components(self):
        layout = QGridLayout()
        layout.addWidget(self.__btn_play, 0, 0)
        layout.addWidget(self.__btn_stop, 0, 1)
        layout.addWidget(self.__tempo_spin_box, 0, 2)
        layout.addWidget(self.__tempo_label, 0, 3)
        layout.addWidget(self.__metronome_checkbox, 1, 0)
        layout.addWidget(self.__metronome_label, 1, 1)
        self.configure_buttons()

        self.__group_box.setLayout(layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.__group_box)
        self.setLayout(main_layout)

    def configure_buttons(self):
        for btn in [self.__btn_play, self.__btn_stop]:
            btn.setFixedSize(100, 100)

    def set_is_playing(self, value):
        self.__is_playing = value

    @property
    def is_playing(self):
        return self.__is_playing

    @property
    def tempo_spinbox(self):
        return self.__tempo_spin_box

    @property
    def btn_play(self):
        return self.__btn_play

    @property
    def btn_stop(self):
        return self.__btn_stop

    @property
    def metronome_checkbox(self):
        return self.__metronome_checkbox




