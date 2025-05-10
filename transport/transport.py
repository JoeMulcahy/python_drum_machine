from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QSpinBox, QLabel, QCheckBox, \
    QDial, QComboBox


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
        self.__time_signature_divider_label = QLabel('/')
        self.__time_signature_label = QLabel('Time signature')
        self.__bpb_spinbox = QSpinBox()
        self.__bpb_spinbox.setRange(1, 12)
        self.__bpb_spinbox.setValue(4)

        self.__beat_type_spinbox = CustomSpinBox([2, 4, 8, 16, 32])
        self.__beat_type_spinbox.setValue(1)

        self.__metronome_volume_dial = QDial()
        self.__metronome_volume_dial.setRange(0, 100)
        self.__metronome_volume_dial.setValue(50)
        self.__metronome_volume_dial.setNotchesVisible(True)
        self.__metronome_volume_dial.setWrapping(False)

        self.initialise_components()

    def initialise_components(self):
        # group boxes
        transport_group_box = QGroupBox(f"Transport")
        tempo_group_box = QGroupBox("Tempo")
        metronome_group_box = QGroupBox("Metronome")

        transport_module_layout = QGridLayout()
        tempo_module_layout = QGridLayout()
        metronome_module_layout = QGridLayout()

        transport_module_layout.setSpacing(20)
        transport_module_layout.addWidget(self.__btn_play, 0, 0)
        transport_module_layout.addWidget(self.__btn_stop, 0, 1)

        tempo_module_layout.addWidget(self.__lbl_bpm, 0, 0)
        tempo_module_layout.addWidget(self.__tempo_spin_box, 0, 1)

        metronome_module_layout.addWidget(self.__time_signature_label, 0, 0, 1, 2)
        metronome_module_layout.addWidget(self.__bpb_spinbox, 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        metronome_module_layout.addWidget(self.__time_signature_divider_label, 0, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        metronome_module_layout.addWidget(self.__beat_type_spinbox, 0, 4, 1, 1, Qt.AlignmentFlag.AlignLeft)

        metronome_module_layout.addWidget(self.__metronome_checkbox, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
        metronome_module_layout.addWidget(self.__metronome_volume_dial, 1, 2, 1, 1)

        transport_group_box.setLayout(transport_module_layout)
        tempo_group_box.setLayout(tempo_module_layout)
        metronome_group_box.setLayout(metronome_module_layout)

        module_layout = QGridLayout()
        module_layout.addWidget(transport_group_box, 0, 0)
        module_layout.addWidget(tempo_group_box, 1, 0)
        module_layout.addWidget(metronome_group_box, 2, 0)

        self.set_style()  # set widgets style

        self.setLayout(module_layout)

    def set_style(self):
        for comp in [self.__btn_play, self.__btn_stop, self.__tempo_spin_box]:
            comp.setFixedSize(100, 50)

        text_style = "QLabel { font-size: 12px; font-weight: bold}"
        self.__metronome_label.setStyleSheet(text_style)
        self.__lbl_bpm.setStyleSheet(text_style)

        self.__metronome_volume_dial.setFixedSize(50, 50)
        self.__metronome_checkbox.setFixedSize(70, 70)

        self.__tempo_spin_box.setStyleSheet("""
            QSpinBox {
                font-size: 24px;       /* Resize text */
                color: #ff5733;        /* Change text color */
            }
        """)

        self.__bpb_spinbox.setStyleSheet("""
            QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
                width: 0;
                height: 0;
                border: none;
            }
        """)
        self.__bpb_spinbox.setFixedSize(30, 20)

        self.__beat_type_spinbox.setStyleSheet("""
                    QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
                        width: 0;
                        height: 0;
                        border: none;
                    }
                """)
        self.__beat_type_spinbox.setFixedSize(30, 20)

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

    @property
    def beat_per_bar_spinbox(self):
        return self.__bpb_spinbox

    @property
    def meter_spinbox(self):
        return self.__beat_type_spinbox


class CustomSpinBox(QSpinBox):
    def __init__(self, values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._values = values
        self._index = 0
        self.setRange(0, len(self._values) - 1)
        self.setValue(0)  # index of the list

    def valueFromText(self, text):
        return self._values.index(int(text))

    def textFromValue(self, value):
        return str(self._values[value])

    def value(self):
        return self._values[super().value()]
