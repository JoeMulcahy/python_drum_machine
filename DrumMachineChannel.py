from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QDial, QGroupBox, QVBoxLayout, QPushButton,
    QComboBox
)

# TODO create a name field that allows the user to name a channel, default name is name of audio file selected
# TODO switch between .wav and digital waveform mode. Will require 2 channel types and channel super class


class DrumMachineChannel(QWidget):
    def __init__(self, channel_index):
        super().__init__()

        self.__channel_id = channel_index
        self.lbl_current_sound = QLabel("Sound: ")

        # channel colors: default, selected
        self.default_channel_color = "QGroupBox { background-color: blue; border: 1px}"
        self.channel_select_color = "QGroupBox { background-color: light-gray; border: 1px}"

        # button colors
        self.button_color = "QPushButton {background-color: #ef1212; color: white;}"

        # groupbox
        self.group_box = QGroupBox(f"Channel: {self.__channel_id}")
        self.group_box.setStyleSheet(self.default_channel_color)

        # combobox with audio file names
        self.__sound_selection_combo_box = QComboBox()
        self.__sound_selection_combo_box.setCurrentIndex(0)

        # sound preview button
        self.__btn_preview_sound = QPushButton("Preview")

        # labels for channel controls
        self.__lbl_volume = QLabel('Volume')
        self.__lbl_pan = QLabel('Pan')
        self.__lbl_pitch = QLabel('Pitch')
        self.__lbl_length = QLabel('Length')
        self.__lbl_duration = QLabel('Stretch')

        # labels for channel control amounts
        self.__lbl_volume_text = QLabel("50%")
        self.__lbl_pan_text = QLabel("50%")
        self.__lbl_pitch_text = QLabel("50%")
        self.__lbl_length_text = QLabel("50%")
        self.__lbl_duration_text = QLabel('50%')

        # channel controls
        self.__dial_volume = QDial()
        self.__dial_pan = QDial()
        self.__dial_pitch = QDial()
        self.__dial_length = QDial()
        self.__dial_duration = QDial()

        # reset pitch, length and time stretch button
        self.__btn_reset = QPushButton("")
        self.__btn_reset.setFixedSize(20, 20)
        self.__btn_reset.setStyleSheet(self.button_color)

        # select channel button
        self.select_channel_button = QPushButton("Select")
        self.select_channel_button.setProperty("id", channel_index)  # channel identifier

        self.init_components()

        # Listeners - change labels to match values of dials
        self.__dial_volume.valueChanged\
            .connect(lambda: self.__lbl_volume_text.setText(str(self.__dial_volume.value()) + "%"))
        self.__dial_pan.valueChanged\
            .connect(lambda: self.__lbl_pan_text.setText(str(self.__dial_pan.value()) + "%"))
        self.__dial_pitch.valueChanged\
            .connect(lambda: self.__lbl_pitch_text.setText(str(self.__dial_pitch.value()) + "%"))
        self.__dial_length.valueChanged\
            .connect(lambda: self.__lbl_length_text.setText(str(self.__dial_length.value()) + "%"))
        self.__dial_duration.valueChanged\
            .connect(lambda: self.__lbl_duration_text.setText(str(self.__dial_duration.value()) + "%"))

        # Listeners - Reset dial value on lbl_text double-click
        self.__lbl_volume_text.mouseDoubleClickEvent = lambda event: self.__dial_volume.setValue(50)
        self.__lbl_pan_text.mouseDoubleClickEvent = lambda event: self.__dial_pan.setValue(50)
        self.__lbl_pitch_text.mouseDoubleClickEvent = lambda event: self.__dial_pitch.setValue(50)
        self.__lbl_length_text.mouseDoubleClickEvent = lambda event: self.__dial_length.setValue(100)
        self.__lbl_duration_text.mouseDoubleClickEvent = lambda event: self.__dial_duration.setValue(50)

    def init_components(self):
        layout = QGridLayout()

        layout.addWidget(self.lbl_current_sound, 0, 0)
        layout.addWidget(self.__sound_selection_combo_box, 0, 1)
        layout.addWidget(self.__btn_preview_sound, 1, 1)

        layout.addWidget(self.__lbl_volume, 2, 0)
        layout.addWidget(self.__dial_volume, 3, 0)
        layout.addWidget(self.__lbl_volume_text, 4, 0)

        layout.addWidget(self.__lbl_pan, 2, 1)
        layout.addWidget(self.__dial_pan, 3, 1)
        layout.addWidget(self.__lbl_pan_text, 4, 1)

        layout.addWidget(self.__lbl_pitch, 5, 0)
        layout.addWidget(self.__dial_pitch, 6, 0)
        layout.addWidget(self.__lbl_pitch_text, 7, 0)

        layout.addWidget(self.__lbl_length, 5, 1)
        layout.addWidget(self.__dial_length, 6, 1)
        layout.addWidget(self.__lbl_length_text, 7, 1)

        layout.addWidget(self.__lbl_duration, 8, 1)
        layout.addWidget(self.__dial_duration, 9, 1)
        layout.addWidget(self.__lbl_duration_text, 10, 1)

        layout.addWidget(self.__btn_reset, 9, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.select_channel_button, 11, 0, 3, 2)

        self.group_box.setLayout(layout)

        # Main layout of this widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

        # Set default dial values
        for dial in [self.__dial_pitch, self.__dial_pan, self.__dial_volume, self.__dial_length, self.__dial_duration]:
            dial.setMinimum(1)
            dial.setMaximum(100)
            dial.setValue(50)
            dial.setFixedSize(50, 50)
            dial.setNotchesVisible(True)
            dial.setWrapping(False)

            if dial == self.__dial_length:
                dial.setValue(100)

        self.setLayout(layout)

    @property
    def sound_selection_combobox(self):
        return self.__sound_selection_combo_box

    @sound_selection_combobox.setter
    def sound_selection_combobox(self, value):
        self.__sound_selection_combo_box = value

    @property
    def volume_value_label(self):
        return self.__lbl_volume_text

    @property
    def pan_value_label(self):
        return self.__lbl_pan_text

    @property
    def pitch_value_label(self):
        return self.__lbl_pitch_text

    @property
    def length_value_label(self):
        return self.__lbl_length_text

    @property
    def duration_value_label(self):
        return self.__lbl_duration_text

    @property
    def preview_button(self):
        return self.__btn_preview_sound

    @property
    def select_button(self):
        return self.select_channel_button

    @property
    def reset_button(self):
        return self.__btn_reset

    @property
    def volume_dial(self):
        return self.__dial_volume

    @property
    def pan_dial(self):
        return self.__dial_pan

    @property
    def pitch_dial(self):
        return self.__dial_pitch

    @property
    def length_dial(self):
        return self.__dial_length

    @property
    def duration_dial(self):
        return self.__dial_duration

    @property
    def channel_id(self):
        return self.__channel_id

    def select_channel(self):
        self.group_box.setStyleSheet(self.channel_select_color)

    def unselect_channel(self):
        self.group_box.setStyleSheet(self.default_channel_color)

    def reset_channel(self):
        self.__dial_pitch.setValue(50)
        self.__dial_length.setValue(100)
        self.__dial_duration.setValue(50)


