from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QDial, QCheckBox, QGroupBox, QGridLayout

import settings


class MetronomeGui(QWidget):
    def __init__(self):
        super().__init__()

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

        self.__beat_type_spinbox = CustomSpinBox([4, 8, 16])
        self.__beat_type_spinbox.setValue(0)

        self.__metronome_volume_dial = QDial()
        self.__metronome_volume_dial.setRange(0, 100)
        self.__metronome_volume_dial.setValue(50)
        self.__metronome_volume_dial.setNotchesVisible(True)
        self.__metronome_volume_dial.setWrapping(False)

        metronome_group_box = QGroupBox("Metronome")
        metronome_module_layout = QGridLayout()

        metronome_module_layout.addWidget(self.__time_signature_label, 0, 0, 1, 2)
        metronome_module_layout.addWidget(self.__bpb_spinbox, 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        metronome_module_layout.addWidget(self.__time_signature_divider_label, 0, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        metronome_module_layout.addWidget(self.__beat_type_spinbox, 0, 4, 1, 1, Qt.AlignmentFlag.AlignLeft)

        metronome_module_layout.addWidget(self.__metronome_checkbox, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
        metronome_module_layout.addWidget(self.__metronome_volume_dial, 1, 2, 1, 1)

        self.set_style()

        metronome_group_box.setLayout(metronome_module_layout)

        module_layout = QGridLayout()
        module_layout.addWidget(metronome_group_box, 0, 0)
        self.setLayout(module_layout)

    def set_style(self):
        self.__metronome_label.setStyleSheet(settings.TEXT_STYLE_1)

        self.__metronome_volume_dial.setFixedSize(50, 50)
        self.__metronome_checkbox.setFixedSize(70, 70)

        self.__bpb_spinbox.setStyleSheet(settings.BEATS_PER_BAR_SPINBOX_STYLING)
        self.__bpb_spinbox.setFixedSize(30, 20)

        self.__beat_type_spinbox.setStyleSheet(settings.BEAT_TYPE_SPINBOX_STYLING)
        self.__beat_type_spinbox.setFixedSize(30, 20)

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
