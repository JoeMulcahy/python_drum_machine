from pathlib import Path

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QDial, QGroupBox, QVBoxLayout, QPushButton,
    QComboBox
)

from enum import Enum

from sound_engine.AudioFile import AudioFile


class ChannelType(Enum):
    KICK = 1,
    SNARE = 2,
    TOM_1 = 3,
    TOM_2 = 4,
    TOM_3 = 5,
    RIM = 6,
    HAND_CLAP = 7,
    COW_BELL = 8,
    CYMBAL_1, = 9,
    CYMBAL_2 = 10,
    HATS_CLOSED = 11,
    HAT_OPEN = 12,
    EXTRA_1 = 13,
    EXTRA_2 = 14,
    EXTRA_3 = 15,
    EXTRA_4 = 16,


# TODO create a name field that allows the user to name a channel, default name is name of audio file selected
# TODO switch between .wav and digital waveform mode. Will require 2 channel types and channel super class


class DrumMachineChannel(QWidget):
    def __init__(self, channel_index):
        super().__init__()
        self.samples_dir = r"C:\Users\josep\Desktop\Step Seq\audio"
        self.audio_samples_list = self.get_audio_samples_list()  # create list of audio samples:
        audio_sample_names = [file.name for file in self.audio_samples_list]  # create list of audio sample names: str
        self.currently_selected_audio_file = self.audio_samples_list[0]  # set current sample to 1st in list
        self.set_current_selected_audio_file(0)

        self.__channel_index = channel_index
        self.lbl_current_sound = QLabel("Sound: ")

        # channel colors: default, selected
        self.default_channel_color = "QGroupBox { background-color: blue; border: 1px solid gray; }"
        self.channel_select_color = "QGroupBox { background-color: light-gray; border: 1px solid gray; }"

        # groupbox
        self.group_box = QGroupBox(f"Channel: {self.__channel_index}")
        self.group_box.setStyleSheet(self.default_channel_color)

        # combobox with audio file names
        self.sound_selection_combo_box = QComboBox()
        self.sound_selection_combo_box.addItems(audio_sample_names)
        self.sound_selection_combo_box.setCurrentIndex(0)

        # sound preview button
        self.btn_preview_sound = QPushButton("Play")

        # labels for channel controls
        self.lbl_volume = QLabel('Volume')
        self.lbl_pan = QLabel('Pan')
        self.lbl_pitch = QLabel('Pitch')
        self.lbl_length = QLabel('Length')
        self.lbl_duration = QLabel('Duration')

        # labels for channel control amounts
        self.lbl_volume_text = QLabel("50%")
        self.lbl_pan_text = QLabel("50%")
        self.lbl_pitch_text = QLabel("50%")
        self.lbl_length_text = QLabel("50%")
        self.lbl_duration_text = QLabel('50%')

        # channel controls
        self.dial_volume = QDial()
        self.dial_pan = QDial()
        self.dial_pitch = QDial()
        self.dial_length = QDial()
        self.dial_duration = QDial()

        self.select_channel_button = QPushButton("Select")
        self.select_channel_button.setProperty("id", channel_index)  # channel identifier

        self.init_components()

        #########################################
        ## Listeners
        #########################################
        self.dial_volume.valueChanged.connect(lambda: self.volume_change())
        self.dial_pan.valueChanged.connect(lambda: self.pan_change())
        self.dial_pitch.valueChanged.connect(lambda: self.pitch_change())
        self.dial_length.valueChanged.connect(lambda: self.length_change())
        self.dial_duration.valueChanged.connect(lambda: self.duration_change())

        # Reset dial value on lbl_text double-click
        self.lbl_volume_text.mouseDoubleClickEvent = lambda event: self.dial_volume.setValue(50)
        self.lbl_pan_text.mouseDoubleClickEvent = lambda event: self.dial_pan.setValue(50)
        self.lbl_pitch_text.mouseDoubleClickEvent = lambda event: self.dial_pitch.setValue(50)
        self.lbl_length_text.mouseDoubleClickEvent = lambda event: self.dial_length.setValue(100)
        self.lbl_duration_text.mouseDoubleClickEvent = lambda event: self.dial_duration.setValue(50)

        # sets currently select audio file to selected combo box index
        self.sound_selection_combo_box.currentIndexChanged.connect(
            lambda: self.set_current_selected_audio_file(self.sound_selection_combo_box.currentIndex()))

        self.btn_preview_sound.pressed.connect(lambda: self.play_sample())

    def init_components(self):
        layout = QGridLayout()

        layout.addWidget(self.lbl_current_sound, 0, 0)
        layout.addWidget(self.sound_selection_combo_box, 0, 1)
        layout.addWidget(self.btn_preview_sound, 1, 1)

        layout.addWidget(self.lbl_volume, 2, 0)
        layout.addWidget(self.dial_volume, 3, 0)
        layout.addWidget(self.lbl_volume_text, 4, 0)

        layout.addWidget(self.lbl_pan, 2, 1)
        layout.addWidget(self.dial_pan, 3, 1)
        layout.addWidget(self.lbl_pan_text, 4, 1)

        layout.addWidget(self.lbl_pitch, 5, 0)
        layout.addWidget(self.dial_pitch, 6, 0)
        layout.addWidget(self.lbl_pitch_text, 7, 0)

        layout.addWidget(self.lbl_length, 5, 1)
        layout.addWidget(self.dial_length, 6, 1)
        layout.addWidget(self.lbl_length_text, 7, 1)

        layout.addWidget(self.lbl_duration, 8, 1)
        layout.addWidget(self.dial_duration, 9, 1)
        layout.addWidget(self.lbl_duration_text, 10, 1)

        layout.addWidget(self.select_channel_button, 11, 0, 3, 2)

        self.group_box.setLayout(layout)

        # Main layout of this widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

        # Set default dial values
        for dial in [self.dial_pitch, self.dial_pan, self.dial_volume, self.dial_length, self.dial_duration]:
            dial.setMinimum(0)
            dial.setMaximum(100)
            dial.setValue(50)
            dial.setNotchesVisible(True)
            dial.setWrapping(False)

            if dial == self.dial_length:
                dial.setValue(100)

        self.volume_change()  # set initial volume to volume dial value
        self.setLayout(layout)

    @property
    def select_button(self):
        return self.select_channel_button

    @property
    def channel_index(self):
        return self.channel_index

    def volume_change(self):
        self.lbl_volume_text.setText(str(self.dial_volume.value()) + "%")
        if self.currently_selected_audio_file is not None:
            self.currently_selected_audio_file.set_volume(float(self.dial_volume.value()) / 100)

    def pan_change(self):
        self.lbl_pan_text.setText(str(self.dial_pan.value()) + "%")
        if self.currently_selected_audio_file is not None:
            self.currently_selected_audio_file.set_pan(float(self.dial_pan.value()) / 100)

    def pitch_change(self):
        self.lbl_pitch_text.setText(str(self.dial_pitch.value()) + "%")
        if self.currently_selected_audio_file is not None:
            self.currently_selected_audio_file.set_sample_rate(float(self.dial_pitch.value()) / 100)

    def length_change(self):
        self.lbl_length_text.setText(str(self.dial_length.value()) + "%")
        if self.currently_selected_audio_file is not None:
            self.currently_selected_audio_file.set_sample_length(float(self.dial_length.value()) / 100)
        print(f"Length changed: {self.dial_length.value()}")

    def duration_change(self):
        self.lbl_duration_text.setText(str(self.dial_duration.value()) + "%")
        if self.currently_selected_audio_file is not None:
            self.currently_selected_audio_file.set_sample_duration(float(self.dial_duration.value()) / 100)

    # Set current audio file for drum machine channel
    # TODO create a string variable for the file path
    def set_current_selected_audio_file(self, index):
        self.currently_selected_audio_file = self.audio_samples_list[index]
        self.currently_selected_audio_file = AudioFile(
            self.currently_selected_audio_file.name,
            self.samples_dir + f"\\{self.currently_selected_audio_file.name}"
        )

    def play_sample(self):
        if self.currently_selected_audio_file is not None:
            self.currently_selected_audio_file.play()

    def select_channel(self):
        # Set background color using setStyleSheet
        self.group_box.setStyleSheet(self.channel_select_color)

    def unselect_channel(self):
        self.group_box.setStyleSheet(self.default_channel_color)

    ####################################################
    ## Create a list of sounds from dir
    ####################################################
    def get_audio_samples_list(self):
        audio_list = list()
        directory = Path(self.samples_dir)
        for file in directory.iterdir():
            if file.is_file():
                audio_list.append(file)

        return audio_list
