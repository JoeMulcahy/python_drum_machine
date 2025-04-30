from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QSpinBox, QLabel, QCheckBox, \
    QDial


class Transport(QWidget):
    def __init__(self):
        super().__init__()
        self.__is_playing = False

        # play/stop buttons
        self.__btn_play = QPushButton("Play")
        self.__btn_stop = QPushButton("Stop")

        # tempo spinbox
        self.__tempo_spin_box = QSpinBox()
        self.__tempo_spin_box.setRange(1, 300)
        self.__tempo_spin_box.setValue(120)

        self.__lbl_bpm = QLabel("bpm")

        # metronome controls
        self.__metronome_checkbox = QCheckBox()
        self.__metronome_checkbox.setChecked(False)
        self.__metronome_checkbox.setText("on/off")
        self.__metronome_label = QLabel("Metronome")
        self.__metronome_volume_dial = QDial()
        self.__metronome_volume_dial.setRange(0, 100)
        self.__metronome_volume_dial.setValue(50)
        self.__metronome_volume_dial.setNotchesVisible(True)
        self.__metronome_volume_dial.setWrapping(False)

        self.initialise_components()

    def initialise_components(self):
        module_group_box = QGroupBox(f"Transport")
        self.set_style()  # set widgets style

        transport_module_layout = QGridLayout()
        transport_module_layout.setSpacing(20)
        transport_module_layout.addWidget(self.__btn_play, 0, 0)
        transport_module_layout.addWidget(self.__btn_stop, 0, 1)
        transport_module_layout.addWidget(self.__lbl_bpm, 1, 0)
        transport_module_layout.addWidget(self.__tempo_spin_box, 1, 1)
        transport_module_layout.addWidget(self.__metronome_label, 2, 0)
        transport_module_layout.addWidget(self.__metronome_checkbox, 3, 0)
        transport_module_layout.addWidget(self.__metronome_volume_dial, 3, 1)

        module_group_box.setLayout(transport_module_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(module_group_box)
        self.setLayout(main_layout)

    def set_style(self):
        for comp in [self.__btn_play, self.__btn_stop, self.__tempo_spin_box]:
            comp.setFixedSize(100, 50)

        text_style = "QLabel { font-size: 12px; font-weight: bold}"
        self.__metronome_label.setStyleSheet(text_style)
        self.__lbl_bpm.setStyleSheet(text_style)

        self.__metronome_volume_dial.setFixedSize(50, 50)

        self.__metronome_checkbox.setFixedSize(50, 50)

        self.__tempo_spin_box.setStyleSheet("""
            QSpinBox {
                font-size: 24px;       /* Resize text */
                color: #ff5733;        /* Change text color */
            }
        """)

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

    @property
    def metronome_volume_dial(self):
        return self.__metronome_volume_dial
