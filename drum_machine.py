import copy
import os
import random
import stat
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from drum_machine_channel import DrumMachineChannel
from global_controls.global_controls import MasterControls
from metronome.metronome import Metronome
from pattern.PatternManger import PatternManager
from sequencer_module.sequencer_module import SequencerModule
from sound_engine.AudioVoice import AudioVoice
from sound_engine.AudioChannel import AudioChannel
from sound_engine.SoundEngine import SoundEngine
from timer.application_timer import ApplicationTimer
from transport.transport import Transport
import settings


def create_timing_resolution_dict():
    d = dict()
    d[0] = [2, 4]
    d[1] = [4, 4]
    d[2] = [8, 4]
    d[3] = [9, 3]
    d[4] = [16, 4]
    d[5] = [18, 3]
    d[6] = [32, 4]
    d[7] = [64, 4]

    return d


class DrumMachine(QWidget):
    def __init__(self):
        super().__init__()
        self.___test_counter = 0

        self.__number_of_steps = 16  # initial number of steps in stepper
        self.__number_of_drum_machine_channels = 10  # number of channels for the drum machine

        self.__drum_machine_channels_list = list()  # list of channel modules
        self.__channel_solo_list = [False for i in range(self.__number_of_drum_machine_channels)]
        self.__channel_mute_list = [False for i in range(self.__number_of_drum_machine_channels)]
        self.__current_selected_drum_machine_channel_index = 0

        self.__timing_resolution_dict = create_timing_resolution_dict()  # dictionary of [bpb, meter] timings

        ######## intention is to have selectable [1-16][17-32][33-48][49-64] steps banks
        self.__steps_banks = 1;

        # initialise SoundEngine
        self.__audio_engine = SoundEngine()

        # initialise audio sample lists
        self.__audio_channels_list = list()  # list of AudioChannels
        self.__samples_dir = settings.ROOT_DIRECTORY + "\\Step Seq\\audio"  # default drum samples directory
        self.__samples_folders = [
            'kick', 'snare', 'hats_close', 'hats_open', 'tom_hi', 'tom_med', 'tom_lo', 'perc', 'crash', 'cymbal'
        ]

        self.__audio_sample_dict = self.__get_audio_list_dict()  # dict for storing .wav file, dict[idx] = channel
        self.__audio_samples_list = self.get_audio_samples_list()  # list of .wav samples

        # initialise timing values and application timer
        self.__tempo = 120
        self.__beats_per_bar = 4
        self.__meter = 4

        self.__flam_timing = 0.0
        self.__swing_timing = 0.0
        self.__humanise_timing = 0.0
        self.__humanise_timing_strength = 0.0

        self.__app_timer = ApplicationTimer(self.__tempo, self.__beats_per_bar, self.__meter)
        self.__app_timer.set_pulse_callback(self.on_pulse)  # init 'pulse' from app_timer

        # initialise pattern manager
        self.__pattern_manager = PatternManager(4, 8, self.__number_of_drum_machine_channels, self.__number_of_steps)
        # self.__pattern_manager.bank_dict = PatternManager.generate_random_banks(
        #     4, 8, self.__number_of_drum_machine_channels, self.__number_of_steps
        # )
        self.__global_pattern_bank_index = 0
        self.__global_pattern_index = 0
        self.__channel_pattern_index = 0

        self.__selected_global_pattern = self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][
            self.__global_pattern_index]

        # layout for various modules in drum machine
        drum_machine_layout = QGridLayout()

        # layout for the step sequencer's audio channels
        channels_layout = QGridLayout()
        channels_layout.setSpacing(5)
        channels_layout.setContentsMargins(5, 10, 5, 10)

        # initialise audio channels, 1 for each drum machine channel. Add each to engine
        # add drum_machine_channels to channels layout
        for i in range(self.__number_of_drum_machine_channels):
            dm_channel = DrumMachineChannel(i)  # drum machine channel
            dm_channel.sound_selection_combobox.addItems(
                [file.name for file in self.__audio_sample_dict[i]])  # popular combobox with sample names
            dm_channel.sound_selection_combobox.setCurrentIndex(i)
            filename = self.__audio_sample_dict[i][0].name
            audio_voice = \
                AudioVoice(
                    self.__samples_dir + "\\" + self.__samples_folders[i] + f"\\{filename}")  # set sample audio voice
            audio_channel = AudioChannel(i, audio_voice, volume=0.5, pan=0.5)
            dm_channel.channel_name_text.setText(filename[:filename.find('.')])  # remove extension from file name
            self.__audio_channels_list.append(audio_channel)
            self.__audio_engine.add_channel(audio_channel)
            self.__drum_machine_channels_list.append(dm_channel)
            channels_layout.addWidget(dm_channel, 0, i)

        # initialise metronome
        self.__metronome_on = False  # metronome on/off flag
        self.__metronome = Metronome()
        self.__metro_audio_channel = AudioChannel(99, self.__metronome.metronome_voice, volume=0.5, pan=0.5)
        self.__audio_engine.add_channel(self.__metro_audio_channel)

        # Transport and SequencerModule
        self.__transport = Transport()
        self.__sequencer_module = SequencerModule(self.__number_of_steps)

        # number of playable steps
        self.__playable_steps = self.__sequencer_module.playable_steps_module.current_number_of_playable_steps

        # select first channel as default
        self.__update_select_channel(self.__current_selected_drum_machine_channel_index)

        # Master Control module
        self.__master_controls = MasterControls()

        # add transport and sequencerModule to layout controls layout
        controls_layout = QGridLayout()
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        controls_layout.addWidget(self.__transport, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__sequencer_module, 0, 1, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)
        controls_layout.addWidget(self.__master_controls, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # add channel and control layouts to drum_machine_layout layout
        drum_machine_layout.addLayout(channels_layout, 0, 0)  # drum machine channels
        drum_machine_layout.addLayout(controls_layout, 1, 0)  # transport, sequencer module

        # add drum machine layout to main layout
        main_layout = QGridLayout()
        main_layout.addLayout(drum_machine_layout, 0, 0)
        self.setLayout(main_layout)

        #####################################################################################################
        ########################## Listeners for drum machine channel module ################################
        #####################################################################################################

        # Listeners for drum machine channel select buttons
        for channel in self.__drum_machine_channels_list:
            select_button = channel.select_button
            select_button.clicked.connect(
                (lambda checked, b=select_button: self.__update_select_channel(b.property("id"))))

        # Listeners for drum machine samples combo box
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            cb = dmc.sound_selection_combobox
            cb.currentIndexChanged.connect(
                lambda index, dmc_i=dmc_index: self.__set_voice_for_drum_machine_channels(index, dmc_i))

        # Listeners for drum machine channel dials [volume, pan, length, pitch, duration]
        for i in range(len(self.__drum_machine_channels_list)):
            self.__drum_machine_channels_list[i].volume_dial.valueChanged \
                .connect(lambda val, index=i: self.__set_channel_volume(index, val))

            self.__drum_machine_channels_list[i].pan_dial.valueChanged \
                .connect(lambda val, index=i: self.__set_channel_pan(index, val))

            self.__drum_machine_channels_list[i].length_dial.valueChanged \
                .connect(lambda val, index=i: self.__set_voice_length(index, val))

            self.__drum_machine_channels_list[i].duration_dial.valueChanged \
                .connect(lambda val, index=i: self.__set_time_stretch(index, val))

            self.__drum_machine_channels_list[i].pitch_dial.valueChanged \
                .connect(lambda val, index=i: self.__set_sample_pitch(index, val))

            self.__drum_machine_channels_list[i].tone_dial.valueChanged \
                .connect(lambda val, index=i: self.__set_sample_tone(index, val))

        # Listener for drum machine channel preview buttons
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.preview_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__play_preview(dmc_i, True))

        # Listener for drum machine channel post preview buttons
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.post_preview_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__play_preview(dmc_i, False))

        # Listener for drum machine channel reset buttons
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.reset_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__reset_channel(dmc_i))

        # Listener for drum machine channel solo buttons
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.solo_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__solo_channels(dmc_i))

        # Listener for drum machine channel mute buttons
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.mute_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__mute_channels(dmc_i))

        # Listener for opening file directory
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.open_file_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__open_files_in_directory(dmc_i))

        #####################################################################################################
        ########################## Listeners for Transport module ###########################################
        #####################################################################################################

        # Listeners for Transport module
        self.__transport.btn_play.clicked.connect(lambda: self.start_engine())
        self.__transport.btn_stop.clicked.connect(lambda: self.stop_engine())
        self.__transport.tempo_spinbox.valueChanged.connect(lambda value: self.set_tempo(value))
        self.__transport.metronome_checkbox.clicked.connect(
            lambda checked: self.set_metronome_on_off(checked)
        )
        self.__transport.metronome_volume_dial.valueChanged.connect(lambda val: self.__set_metronome_volume(val))

        #####################################################################################################
        ########################## Listeners for pattern selection ################################
        #####################################################################################################

        # Listener for (global) pattern select
        for btn in self.__sequencer_module.pattern_select.buttons_list:
            btn.clicked.connect(lambda checked, b=btn: self.__update_global_pattern_index(int(b.text())))

        # Listener for bank select
        temp_counter = 0
        for btn in self.__sequencer_module.pattern_select.bank_buttons_list:
            btn.clicked.connect(lambda checked, index=temp_counter: self.__update_bank_index(index))
            temp_counter = temp_counter + 1

        self.__sequencer_module.pattern_select.copy_button.clicked.connect(
            lambda: self.__copy_global_pattern()
        )

        self.__sequencer_module.pattern_select.paste_button.clicked.connect(
            lambda: self.__paste_global_pattern()
        )

        #####################################################################################################
        ########################## Listeners for Playable Steps module ######################################
        #####################################################################################################
        self.__sequencer_module.playable_steps_module.playable_steps_spinbox.valueChanged.connect(
            lambda val: self.__set_playable_steps(val)
        )

        #####################################################################################################
        ########################## Listeners for Timings module ##########################################
        #####################################################################################################

        # Listener for Timing resolution module
        self.__sequencer_module.timing_resolution_select. \
            timing_select_dial.valueChanged.connect(lambda index: self.set_timing_resolution(index))

        self.__sequencer_module.timing_resolution_select. \
            flam_dial.valueChanged.connect(lambda val: self.__set_flam(val))

        self.__sequencer_module.timing_resolution_select. \
            swing_dial.valueChanged.connect(lambda val: self.__set_swing(val))

        self.__sequencer_module.timing_resolution_select. \
            humanise_dial.valueChanged.connect(lambda val: self.__set_humanise(val))

        #####################################################################################################
        ########################## Listeners for Master Controls ############################################
        #####################################################################################################
        self.__master_controls.volume_dial.valueChanged.connect(lambda val: self.__set_master_volume(val))
        self.__master_controls.load_profile_button.clicked.connect(lambda: self.__load_profile())
        self.__master_controls.save_profile_button.clicked.connect(lambda: self.__save_profile())
        self.__master_controls.un_mute_all.clicked.connect(lambda: self.__unmute_all())
        self.__master_controls.un_solo_all.clicked.connect(lambda: self.__unsolo_all())

        #####################################################################################################
        ########################## Listeners for stepper controls ############################################
        #####################################################################################################
        self.__sequencer_module.stepper.shift_left_button.clicked.connect(lambda: self.__shift_pattern_left())
        self.__sequencer_module.stepper.shift_right_button.clicked.connect(lambda: self.__shift_pattern_right())
        self.__sequencer_module.stepper.clear_button.clicked.connect(lambda: self.__clear_pattern())
        self.__sequencer_module.stepper.generate_pattern_button.clicked.connect(lambda: self.__generate_pattern())
        self.__sequencer_module.stepper.generate_random_pattern_button.clicked.connect(
            lambda: self.__generate_random_pattern())
        self.__sequencer_module.stepper.invert_pattern_button.clicked.connect(lambda: self.__invert_pattern())
        self.__sequencer_module.stepper.copy_button.clicked.connect(lambda: self.__copy_pattern())
        self.__sequencer_module.stepper.paste_button.clicked.connect(lambda: self.__paste_pattern())

    ########################################################################
    # Take action upon receiving pulse from app_timer
    ########################################################################
    def on_pulse(self, pulse_counter):
        self.__sequencer_module.stepper.stepper_indicators_on_play(pulse_counter)
        self.trigger_audio(pulse_counter)

    def trigger_audio(self, count):
        pattern_to_play = []
        for i in range(len(self.__selected_global_pattern)):
            pattern_to_play.append(self.__selected_global_pattern[i][count % self.__playable_steps])

        # Calculate the time at which the sound should be triggered.
        # trigger_time = count * (60.0 / self.__tempo)  # Convert count to time based on BPM
        # current_time = self.__audio_engine.get_current_time()
        delay = 0
        if self.__humanise_timing_strength > 0:
            self.__calculate_humanise_timing()

        if count % 2 == 0:
            delay = self.__flam_timing + self.__humanise_timing
        elif count % 2 == 1:
            delay = self.__swing_timing + self.__humanise_timing

        for i in range(len(self.__audio_channels_list)):
            if pattern_to_play[i] == 1:
                if self.__humanise_timing > 0.0 or self.__flam_timing > 0.0 or self.__swing_timing > 0.0:
                    threading.Timer(delay, self.__audio_channels_list[i].trigger).start()
                else:
                    self.__audio_channels_list[i].trigger()

        if self.__metronome_on:
            self.__metro_audio_channel.voice = self.__metronome.metronome_tick_voice(count)
            self.__metro_audio_channel.trigger()

    def start_engine(self):
        self.__audio_engine.play()
        self.__app_timer.start_counter()

    def stop_engine(self):
        self.__audio_engine.stop()
        self.__sequencer_module.stepper.current_stepper_buttons_selected(self.__current_pattern)
        self.__sequencer_module.stepper.reset_stepper_indicators()
        self.__app_timer.stop_counter()

    # Transport methods
    def __set_metronome_volume(self, value):
        self.__metro_audio_channel.volume = value / 100

    def set_tempo(self, value):
        self.__app_timer.set_tempo(int(value))

    def set_metronome_on_off(self, is_on):
        self.__metronome_on = is_on

    def __set_playable_steps(self, value):
        self.__playable_steps = value
        self.__sequencer_module.stepper.number_of_playable_steps = value

    def set_time_resolution(self, bpb, meter):
        self.__app_timer.set_timing_resolution(bpb, meter)

    def set_timing_resolution(self, index):
        index = index - 1
        self.set_time_resolution(self.__timing_resolution_dict[index][0], self.__timing_resolution_dict[index][1])
        self.__metronome.meter = self.__timing_resolution_dict[index][1]
        self.__metronome.beats_per_bar = self.__timing_resolution_dict[index][0]

    def __set_flam(self, value):
        if value > 0:
            delay = self.__app_timer.interval * (value / 100)
            self.__flam_timing = delay
        else:
            self.__flam_timing = 0.0

    def __set_swing(self, value):
        if value > 0:
            delay = self.__app_timer.interval * (value / 100)
            self.__swing_timing = delay
        else:
            self.__swing_timing = 0.0

    def __set_humanise(self, value):
        if value > 0:
            self.__humanise_timing_strength = value / 100
        else:
            self.__humanise_timing = 0.0
            self.__humanise_timing_strength = 0.0

    def __calculate_humanise_timing(self):
        delay = random.uniform(0.0, self.__app_timer.interval) * self.__humanise_timing_strength
        self.__humanise_timing = delay

    def __update_bank_index(self, index):
        self.__global_pattern_bank_index = index
        self.__update_current_pattern()

    def __update_global_pattern_index(self, index):
        self.__global_pattern_index = index - 1
        self.__update_current_pattern()

    # highlight channel upon selection
    # select pattern associated with selected channel and update pattern on the stepper
    def __update_select_channel(self, btn_id):
        index = int(btn_id)
        for channel in self.__drum_machine_channels_list:
            channel.unselect_channel()

        channel = self.__drum_machine_channels_list[index]
        channel.select_channel()

        self.__channel_pattern_index = index
        self.__update_current_pattern()

    def __update_current_pattern(self):
        self.__current_pattern = \
            self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
                self.__channel_pattern_index]
        self.__selected_global_pattern = self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][
            self.__global_pattern_index]
        self.__update_stepper_display()

    def __update_stepper_display(self):
        print(f'{self.__global_pattern_bank_index}{self.__global_pattern_index}{self.__channel_pattern_index}')
        self.__sequencer_module.stepper.current_stepper_buttons_selected(self.__current_pattern)

    # stepper control methods
    def __copy_pattern(self):
        self.__pattern_manager.temp_local_pattern = self.__current_pattern
        print(f'copied: {self.__pattern_manager.temp_local_pattern}')

    def __paste_pattern(self):
        # if list not empty and does not contain all 0's
        # if not self.__pattern_manager.temp_local_pattern and not self.__pattern_manager.temp_local_pattern == [0 for i in range(self.__number_of_steps)]:
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = self.__pattern_manager.temp_local_pattern
        self.__update_current_pattern()

    def __shift_pattern_left(self):
        temp_pattern = PatternManager.shift_pattern_left(self.__current_pattern, amount=1)
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = temp_pattern
        self.__update_current_pattern()

    def __shift_pattern_right(self):
        temp_pattern = PatternManager.shift_pattern_right(self.__current_pattern, amount=1)
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = temp_pattern
        self.__update_current_pattern()

    def __invert_pattern(self):
        temp_pattern = PatternManager.invert_pattern(self.__current_pattern)
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = temp_pattern
        self.__update_current_pattern()

    def __clear_pattern(self):
        temp_pattern = PatternManager.clear_pattern(self.__current_pattern)
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = temp_pattern
        self.__update_current_pattern()

    def __generate_pattern(self):
        number_of_steps = self.__sequencer_module.stepper.number_of_steps
        freq = self.__sequencer_module.stepper.step_freq_spinbox.value()
        temp_pattern = PatternManager.generate_sequenced_pattern(number_of_steps, freq)
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = temp_pattern
        self.__update_current_pattern()

    def __generate_random_pattern(self):
        temp_pattern = PatternManager.generate_random_pattern()
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
            self.__channel_pattern_index] = temp_pattern
        self.__update_current_pattern()

    # pattern select methods
    def __copy_global_pattern(self):
        self.__pattern_manager.temp_global_pattern = copy.deepcopy(
            self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][
                self.__global_pattern_index])

    def __paste_global_pattern(self):
        self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][
            self.__global_pattern_index] = self.__pattern_manager.temp_global_pattern
        self.__update_current_pattern()

    # drum machine channel methods
    def __play_preview(self, index, is_pre):
        self.__audio_channels_list[index].voice.preview_voice(is_pre)

    def __set_voice_for_drum_machine_channels(self, index, dmc_index):
        print(f'debug combo values: {self.__audio_sample_dict[dmc_index]}')
        filename = self.__audio_sample_dict[dmc_index][index]
        voice = AudioVoice(filename)
        self.__audio_channels_list[dmc_index].voice = voice
        print(f'{self.__audio_channels_list[dmc_index].voice}')
        print(f'\n\n')

    def __set_channel_volume(self, index, value):
        self.__audio_channels_list[index].volume = value / 100

    def __set_channel_pan(self, index, value):
        self.__audio_channels_list[index].pan = value / 100

    def __set_voice_length(self, index, value):
        self.__audio_channels_list[index].voice.set_voice_length(value / 100)

    def __set_sample_pitch(self, index, value):
        self.__audio_channels_list[index].voice.set_pitch(value / 100)

    def __set_time_stretch(self, index, value):
        self.__audio_channels_list[index].voice.set_time_stretch(value / 100)

    def __set_sample_tone(self, index, value):
        self.__audio_channels_list[index].set_hsf_gain(value)

    def __reset_channel(self, index):
        self.__audio_channels_list[index].voice.reset_voice()
        self.__drum_machine_channels_list[index].reset_channel()

    def __solo_channels(self, index):
        if self.__channel_mute_list[index]:
            self.__channel_mute_list[index] = False
            self.__drum_machine_channels_list[index].set_mute_on(False)

        if not self.__channel_solo_list[index]:
            self.__channel_solo_list[index] = True
            self.__drum_machine_channels_list[index].set_solo_on(True)
        elif self.__channel_solo_list[index]:
            self.__channel_solo_list[index] = False
            self.__drum_machine_channels_list[index].set_solo_on(False)

        self.__mute_audio_channels()

    def __mute_channels(self, index):
        if self.__channel_solo_list[index]:
            self.__channel_solo_list[index] = False
            self.__drum_machine_channels_list[index].set_solo_on(False)

        if not self.__channel_mute_list[index]:
            self.__channel_mute_list[index] = True
            self.__drum_machine_channels_list[index].set_mute_on(True)
        elif self.__channel_mute_list[index]:
            self.__channel_mute_list[index] = False
            self.__drum_machine_channels_list[index].set_mute_on(False)

        self.__mute_audio_channels()

    # used by solo and mute buttons
    def __mute_audio_channels(self):
        # check if solo list has a True value before inversion
        # inversion mutes any channel that hasn't been soloed
        invert_solo = []
        for val in self.__channel_solo_list:
            if val:
                invert_solo = [False if val else True for val in self.__channel_solo_list]
                break
            else:
                invert_solo = self.__channel_solo_list

        # combine inverted solo and mute list
        to_muted = [a or b for a, b in zip(invert_solo, self.__channel_mute_list)]
        for i in range(self.__number_of_drum_machine_channels):
            if to_muted[i]:
                self.__audio_channels_list[i].is_muted = True
            else:
                self.__audio_channels_list[i].is_muted = False

    # Global Controls methods
    def __set_master_volume(self, value):
        self.__audio_engine.set_master_volume(value / 100)

    def __unmute_all(self):
        for i in range(self.__number_of_drum_machine_channels):
            if self.__channel_mute_list[i]:
                self.__mute_channels(i)

    def __unsolo_all(self):
        for i in range(self.__number_of_drum_machine_channels):
            if self.__channel_solo_list[i]:
                self.__solo_channels(i)

    def __load_profile(self):
        print(f"Load profile")

    def __save_profile(self):
        print(f"Save profile")

    def __open_files_in_directory(self, index):
        root = tk.Tk()
        root.withdraw()  # Hide main window

        folder_path = filedialog.askdirectory(initialdir=r"C:\Users\josep\Desktop\Step Seq\audio",
                                              title="Choose .wav files in directory")

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        directory = Path(folder_path)

        if folder_path:
            try:
                print(f'PRE Audio in dict at index: {index}\n{self.__audio_sample_dict[index]}')
                audio_list = []
                self.__drum_machine_channels_list[index].sound_selection_combobox.clear()
                for file in directory.iterdir():
                    if file.is_file():
                        audio_list.append(file)
                        self.__drum_machine_channels_list[index].sound_selection_combobox \
                            .addItem(f"{file.name}")

                self.__audio_sample_dict[index] = copy.deepcopy(audio_list)
                filename = self.__audio_sample_dict[index][0].name
                voice = AudioVoice(folder_path + f"\\{filename}")
                self.__audio_channels_list[index].voice = voice
                print(f'{self.__audio_channels_list[index].voice}')

            except FileNotFoundError:
                print(f'Folder not found at {directory}')
            except Exception as e:
                print(f'Error!!!!!!!!!!!!!!!!!!!!: {e}')
        else:
            print("No folder selected")

    def __get_audio_list_dict(self):
        directory = Path(self.__samples_dir)
        samples_dict = dict()

        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a valid directory!")

        for i in range(len(self.__samples_folders)):
            audio_list = []
            sample_dir = Path(f"{directory}/{self.__samples_folders[i]}")
            try:
                for file in sample_dir.iterdir():
                    if file.is_file():
                        audio_list.append(file)

                    samples_dict[i] = audio_list
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error when scanning directory: {e}")

        print(samples_dict)
        return samples_dict

    ####################################################
    ## Create a list of sounds from dir
    ####################################################
    def get_audio_samples_list(self):
        directory = Path(self.__samples_dir)

        # mode = os.stat(self.__samples_dir).st_mode
        # print("Is directory:", stat.S_ISDIR(mode))
        # print("Is readable:", os.access(self.__samples_dir, os.R_OK))
        # print("Is writable:", os.access(self.__samples_dir, os.W_OK))

        folders = ['crash', 'cymbal', 'hats_close', 'hats_open', 'kick', 'perc', 'snare', 'tom_hi', 'tom_med', 'tom_lo']

        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a valid directory!")

        audio_list = []
        try:
            for file in directory.iterdir():
                if file.is_file():
                    audio_list.append(file)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error when scanning directory: {e}")

        return audio_list
