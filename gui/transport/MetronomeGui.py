from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QDial, QCheckBox

from gui.transport.transport_tempo_gui import CustomSpinBox


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