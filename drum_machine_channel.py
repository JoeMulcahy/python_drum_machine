from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QDial, QGroupBox, QVBoxLayout, QPushButton,
    QComboBox, QLineEdit, QSizePolicy
)


# TODO create a name field that allows the user to name a channel, default name is name of audio file selected
# TODO switch between .wav and digital waveform mode. Will require 2 channel types and channel super class


class DrumMachineChannel(QWidget):
    def __init__(self, channel_index):
        super().__init__()

        self.__channel_id = channel_index

        # layout size policy
        self.__size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # groupbox
        self.__group_box = QGroupBox()

        # name text box
        self.__name_textbox = QLineEdit()

        # open file button
        self.__btn_open_file = QPushButton()
        self.__btn_open_file.setIcon(QIcon("images/folder.png"))

        # combobox with audio file names
        self.__sound_selection_combo_box = QComboBox()
        self.__sound_selection_combo_box.setCurrentIndex(0)
        # self.__sound_selection_combo_box.setFixedSize(80, 25)

        # labels for channel controls
        self.__lbl_volume = QLabel('Vol')
        self.__lbl_pan = QLabel('Pan')
        self.__lbl_pitch = QLabel('Pitch')
        self.__lbl_length = QLabel('Len')
        self.__lbl_duration = QLabel('Stretch')
        self.__lbl_tone = QLabel('Tone')
        self.__lbl_preview = QLabel('Preview')

        # labels for channel control amounts
        self.__lbl_volume_text = QLabel("50%")
        self.__lbl_pan_text = QLabel("50%")
        self.__lbl_pitch_text = QLabel("50%")
        self.__lbl_length_text = QLabel("50%")
        self.__lbl_duration_text = QLabel('50%')
        self.__lbl_tone_text = QLabel('50%')

        # channel controls
        self.__dial_volume = QDial()
        self.__dial_pan = QDial()
        self.__dial_pitch = QDial()
        self.__dial_length = QDial()
        self.__dial_duration = QDial()
        self.__dial_tone = QDial()

        # mute, solo buttons
        self.__btn_solo = QPushButton("S")
        self.__btn_mute = QPushButton("M")

        # reset pitch, length and time stretch button
        self.__btn_reset = QPushButton("R")
        self.__btn_reset.setFixedSize(20, 20)

        # sound preview button
        self.__btn_preview_sound = QPushButton("Pre")
        self.__btn_post_preview_sound = QPushButton("Post")

        # channel number
        self.__lbl_channel_number = QLabel(f"{self.__channel_id + 1}")

        # select channel button
        self.select_channel_button = QPushButton("Select")
        self.select_channel_button.setProperty("id", channel_index)  # channel identifier

        # channel colors: default, selected
        self.__default_channel_color = "QGroupBox { background-color: #23224a; border: 1px solid gray}"
        self.__channel_select_color = "QGroupBox { background-color: #5957ba; border: 1px solid gray}"

        # button colors
        self.__reset_button_color = "QPushButton {font-size: 9px;  font-weight: bold; background-color: #c41431; color: white;}"
        self.__default_button_color = "QPushButton {font-size: 9px;  font-weight: bold; background-color: #1f2e23; color: white;}"
        self.__solo_button_color_on = "QPushButton {font-size: 9px;  font-weight: bold; background-color: #14c443; color: white;}"
        self.__mute_button_color_on = "QPushButton {font-size: 9px;  font-weight: bold; background-color: #bbc414; color: white;}"

        self.__channel_number_style = "QLabel { font-size: 16px; font-weight: bold; color: #aaaaaa; }"
        self.__channel_number__highlight_style = "QLabel { font-size: 16px; font-weight: bold; color: #cc2216; }"

        self.init_components()

        # Listeners - change labels to match values of dials
        self.__dial_volume.valueChanged \
            .connect(lambda: self.__lbl_volume_text.setText(str(self.__dial_volume.value()) + "%"))
        self.__dial_pan.valueChanged \
            .connect(lambda: self.__lbl_pan_text.setText(str(self.__dial_pan.value()) + "%"))
        self.__dial_pitch.valueChanged \
            .connect(lambda: self.__lbl_pitch_text.setText(str(self.__dial_pitch.value()) + "%"))
        self.__dial_length.valueChanged \
            .connect(lambda: self.__lbl_length_text.setText(str(self.__dial_length.value()) + "%"))
        self.__dial_duration.valueChanged \
            .connect(lambda: self.__lbl_duration_text.setText(str(self.__dial_duration.value()) + "%"))
        self.__dial_tone.valueChanged \
            .connect(lambda: self.__lbl_tone_text.setText(str(self.__dial_tone.value()) + "%"))

        # Listeners - Reset dial value on lbl_text double-click
        self.__lbl_volume_text.mouseDoubleClickEvent = lambda event: self.__dial_volume.setValue(50)
        self.__lbl_pan_text.mouseDoubleClickEvent = lambda event: self.__dial_pan.setValue(50)
        self.__lbl_pitch_text.mouseDoubleClickEvent = lambda event: self.__dial_pitch.setValue(50)
        self.__lbl_length_text.mouseDoubleClickEvent = lambda event: self.__dial_length.setValue(100)
        self.__lbl_duration_text.mouseDoubleClickEvent = lambda event: self.__dial_duration.setValue(50)
        self.__lbl_tone_text.mouseDoubleClickEvent = lambda event: self.__dial_tone.setValue(50)

    def init_components(self):
        layout = QGridLayout()
        layout.setSpacing(2)

        #####################################################
        layout.addWidget(self.__name_textbox, 0, 0, 1, 3)
        layout.addWidget(self.__btn_open_file, 1, 0, 1, 1)
        layout.addWidget(self.__sound_selection_combo_box, 1, 1, 1, 2, Qt.AlignmentFlag.AlignLeft)

        #####################################################
        layout.addWidget(self.__lbl_volume, 2, 0, 1, 1)
        layout.addWidget(self.__dial_volume, 3, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__lbl_volume_text, 4, 0, 1, 1)

        layout.addWidget(self.__lbl_pan, 2, 1, 1, 1)
        layout.addWidget(self.__dial_pan, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__lbl_pan_text, 4, 1, 1, 1)

        layout.addWidget(self.__lbl_tone, 2, 2, 1, 1)
        layout.addWidget(self.__dial_tone, 3, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__lbl_tone_text, 4, 2, 1, 1)

        #####################################################
        layout.addWidget(self.__lbl_pitch, 5, 0, 1, 1)
        layout.addWidget(self.__dial_pitch, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__lbl_pitch_text, 7, 0, 1, 1)

        layout.addWidget(self.__lbl_length, 5, 1, 1, 1)
        layout.addWidget(self.__dial_length, 6, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__lbl_length_text, 7, 1, 1, 1)

        layout.addWidget(self.__lbl_duration, 5, 2, 1, 1)
        layout.addWidget(self.__dial_duration, 6, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__lbl_duration_text, 7, 2, 1, 1)

        #######################################################
        layout.addWidget(self.__btn_solo, 8, 0, 1, 1)
        layout.addWidget(self.__btn_mute, 8, 1, 1, 1)
        layout.addWidget(self.__btn_reset, 8, 2, 1, 1)

        #######################################################
        layout.addWidget(self.__lbl_preview, 9, 0, 1, 1)
        layout.addWidget(self.__btn_preview_sound, 9, 1, 1, 1)
        layout.addWidget(self.__btn_post_preview_sound, 9, 2, 1, 1)

        #######################################################
        layout.addWidget(self.__lbl_channel_number, 10, 0, 1, 1)
        layout.addWidget(self.select_channel_button, 10, 1, 1, 2)

        self.__group_box.setLayout(layout)

        # Main layout of this widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.__group_box)
        self.setLayout(main_layout)

        # Set size for buttons in channel
        for btn in [self.__btn_solo, self.__btn_mute, self.__btn_reset, self.__btn_open_file,
                    self.__btn_post_preview_sound, self.__btn_preview_sound]:
            btn.setFixedSize(25, 25)
            btn.setStyleSheet(self.__default_button_color)
            btn.setSizePolicy(self.__size_policy)

            if btn == self.__btn_reset:
                btn.setStyleSheet(self.__reset_button_color)

        # label style
        label_style = "QLabel { font-size: 9px; font-weight: bold; color: #aaaaaa; }"
        for label in self.findChildren(QWidget):
            label.setSizePolicy(self.__size_policy)
            if isinstance(label, QLabel):
                label.setStyleSheet(label_style)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__lbl_channel_number.setStyleSheet(self.__channel_number_style)

        # LineEdit style
        textbox_style = "QLineEdit { font-size: 10px; color: #aaaaaa; font-weight: bold; }"
        self.__name_textbox.setStyleSheet(textbox_style)

        # Set default dial values
        for dial in [self.__dial_pitch, self.__dial_pan, self.__dial_volume, self.__dial_length, self.__dial_duration,
                     self.__dial_tone]:
            dial.setMinimum(1)
            dial.setMaximum(100)
            dial.setValue(50)
            dial.setFixedSize(35, 35)
            dial.setNotchesVisible(True)
            dial.setWrapping(False)

            if dial == self.__dial_length:
                dial.setValue(100)

        self.setLayout(layout)

    def highlight_channel_number(self, is_on):
        if is_on:
            self.__lbl_channel_number.setStyleSheet(self.__channel_number__highlight_style)
        else:
            self.__lbl_channel_number.setStyleSheet(self.__channel_number_style)

    def set_solo_on(self, is_on):
        if is_on:
            self.__btn_solo.setStyleSheet(self.__solo_button_color_on)
        else:
            self.__btn_solo.setStyleSheet(self.__default_button_color)

    def set_mute_on(self, is_on):
        if is_on:
            self.__btn_mute.setStyleSheet(self.__mute_button_color_on)
        else:
            self.__btn_mute.setStyleSheet(self.__default_button_color)

    # channel number label
    @property
    def channel_number_label(self):
        return self.__lbl_channel_number

    # channel id
    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, value):
        self.__channel_id = value

    # channel name
    @property
    def channel_name_text(self):
        return self.__name_textbox

    @channel_name_text.setter
    def channel_name_text(self, value):
        self.__name_textbox.setText(value)

    # samples combo box
    @property
    def sound_selection_combobox(self):
        return self.__sound_selection_combo_box

    @sound_selection_combobox.setter
    def sound_selection_combobox(self, value):
        self.__sound_selection_combo_box = value

    @property
    def combobox_index(self):
        return self.sound_selection_combobox.currentIndex()

    @combobox_index.setter
    def combobox_index(self, value):
        self.sound_selection_combobox.setCurrentIndex(value)

    # channel volume
    @property
    def volume_value_label(self):
        return self.__lbl_volume_text

    @volume_value_label.setter
    def volume_value_label(self, value):
        self.__lbl_volume_text.setText(value)

    @property
    def volume_dial(self):
        return self.__dial_volume

    @volume_dial.setter
    def volume_dial(self, value):
        self.__dial_volume.setValue(value)

    # channel pan
    @property
    def pan_value_label(self):
        return self.__lbl_pan_text

    @pan_value_label.setter
    def pan_value_label(self, value):
        self.__lbl_pan_text.setText(value)

    @property
    def pan_dial(self):
        return self.__dial_pan

    @pan_dial.setter
    def pan_dial(self, value):
        self.__dial_pan.setValue(value)

    # channel tone
    @property
    def tone_value_label(self):
        return self.__lbl_tone_text

    @tone_value_label.setter
    def tone_value_label(self, value):
        self.__lbl_tone_text.setText(value)

    @property
    def tone_dial(self):
        return self.__dial_tone

    @tone_dial.setter
    def tone_dial(self, value):
        self.__dial_tone.setValue(value)

    # channel pitch
    @property
    def pitch_value_label(self):
        return self.__lbl_pitch_text

    @pitch_value_label.setter
    def pitch_value_label(self, value):
        self.__lbl_pitch_text.setText(value)

    @property
    def pitch_dial(self):
        return self.__dial_pitch

    @pitch_dial.setter
    def pitch_dial(self, value):
        self.__dial_pitch.setValue(value)

    # channel sample length
    @property
    def length_value_label(self):
        return self.__lbl_length_text

    @length_value_label.setter
    def length_value_label(self, value):
        self.__lbl_length_text.setText(value)

    @property
    def length_dial(self):
        return self.__dial_length

    @length_dial.setter
    def length_dial(self, value):
        self.__dial_length.setValue(value)

    # channel sample stretch
    @property
    def duration_value_label(self):
        return self.__lbl_duration_text

    @duration_value_label.setter
    def duration_value_label(self, value):
        self.__lbl_duration_text.setText(value)

    @property
    def duration_dial(self):
        return self.__dial_duration

    @duration_dial.setter
    def duration_dial(self, value):
        self.__dial_duration.setValue(value)

    @property
    def open_file_button(self):
        return self.__btn_open_file

    @property
    def preview_button(self):
        return self.__btn_preview_sound

    @property
    def post_preview_button(self):
        return self.__btn_post_preview_sound

    @property
    def solo_button(self):
        return self.__btn_solo

    @property
    def mute_button(self):
        return self.__btn_mute

    @property
    def select_button(self):
        return self.select_channel_button

    @property
    def reset_button(self):
        return self.__btn_reset

    @property
    def length_dial(self):
        return self.__dial_length

    @property
    def duration_dial(self):
        return self.__dial_duration

    @property
    def tone_dial(self):
        return self.__dial_tone

    def select_channel(self):
        self.__group_box.setStyleSheet(self.__channel_select_color)

    def unselect_channel(self):
        self.__group_box.setStyleSheet(self.__default_channel_color)

    def reset_channel(self):
        self.__dial_pitch.setValue(50)
        self.__dial_length.setValue(100)
        self.__dial_duration.setValue(50)
