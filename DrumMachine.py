import os
import stat
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from DrumMachineChannel import DrumMachineChannel
from pattern.Pattern_Manger import PatternManager
from sequencer_module.SequencerModule import SequencerModule
from sound_engine.AudioVoice import AudioVoice
from sound_engine.AudioChannel import Channel
from sound_engine.SoundEngine import SoundEngine
from timer.ApplicationTimer import ApplicationTimer
from transport_module.Transport import Transport


def create_timing_resolution_dict():
    d = dict()
    d[0] = [2, 4]
    d[1] = [4, 4]
    d[2] = [8, 4]
    d[3] = [8, 3]
    d[4] = [16, 4]
    d[5] = [16, 3]
    d[6] = [32, 4]
    d[7] = [64, 4]

    return d


class DrumMachine(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_number_of_steps = 16  # initial number of steps in stepper
        # self.__current_global_pattern = list()  # pattern select (PatternSelect.py)

        self.__drum_machine_channels_list = list()  # list of channel modules
        self.__current_selected_drum_machine_channel_index = 0

        self.__tempo = 120
        self.__beats_per_bar = 4
        self.__meter = 4

        self.__timing_resolution_dict = create_timing_resolution_dict()  # dictionary of [bpb, meter] timings

        self.__metronome_on = False  # metronome on/off flag

        # initialise SoundEngin
        audio_engine = SoundEngine()

        # pattern manager
        self.__pattern_manager = PatternManager()
        self.__bank_index = 0
        self.__global_pattern_bank_index = 0
        self.__global_pattern_index = 0
        self.__channel_pattern_index = 0

        # self.__update_current_pattern()

        self.__audio_channels_list = list()  # list of AudioChannel
        self.__samples_dir = r"C:\Users\josep\Desktop\Step Seq\audio"  # samples location
        self.__audio_samples_list = self.get_audio_samples_list()  # list of .wav samples

        self.__number_of_drum_machine_channels = 8  # number of channels for the drum machine

        # initialise application timer
        self.__app_timer = ApplicationTimer(120, 4, 4)
        self.__app_timer.set_pulse_callback(self.on_pulse)  # receive a 'pulse' from app_timer

        # layout for various modules in drum machine
        drum_machine_layout = QGridLayout()

        # layout for the step sequencer's audio channels
        channels_layout = QGridLayout()
        channels_layout.setSpacing(15)
        channels_layout.setContentsMargins(10, 10, 10, 10)

        # layout for transport, step sequencer modules
        controls_layout = QGridLayout()
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(10, 10, 10, 10)

        # create 8 drum machine channels and add to layout
        # create 8 audio channels, 1 for each drum machine channel. Add each to engine
        # add drum_machine_channels to channels layout
        # TODO might have to create list of created channels in audio engine??
        for i in range(self.__number_of_drum_machine_channels):
            dm_channel = DrumMachineChannel(i)
            dm_channel.sound_selection_combobox.addItems(
                [file.name for file in self.__audio_samples_list])  # popular combobox with sample names
            audio_voice = AudioVoice(self.__samples_dir + f"\\{self.__audio_samples_list[0].name}")
            audio_channel = Channel(i, audio_voice, volume=0.5, pan=0.5)
            self.__audio_channels_list.append(audio_channel)
            audio_engine.add_channel(audio_channel)
            self.__drum_machine_channels_list.append(dm_channel)
            channels_layout.addWidget(dm_channel, 0, i)

        # Transport and SequencerModule
        self.__transport = Transport()
        self.__sequencer_module = SequencerModule(self.__init_number_of_steps)

        # select first channel as default
        self.__update_select_channel(self.__current_selected_drum_machine_channel_index)

        # add transport and sequencerModule to layout controls layout
        controls_layout.addWidget(self.__transport, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__sequencer_module, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        controls_layout.setColumnStretch(0, 2)
        controls_layout.setColumnStretch(1, 5)

        # add channel and control layouts to drum_machine_layout layout
        drum_machine_layout.addLayout(channels_layout, 0, 0)
        drum_machine_layout.addLayout(controls_layout, 1, 0)

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
                .connect(lambda val: self.__set_channel_volume(i, val))
            self.__drum_machine_channels_list[i].pan_dial.valueChanged \
                .connect(lambda val: self.__set_channel_pan(i, val))
            self.__drum_machine_channels_list[i].length_dial.valueChanged \
                .connect(lambda val: self.__set_sample_length(i, val))
            self.__drum_machine_channels_list[i].duration_dial.valueChanged \
                .connect(lambda val: self.__set_sample_duration(i, val))
            self.__drum_machine_channels_list[i].pitch_dial.valueChanged \
                .connect(lambda val: self.__set_sample_pitch(i, val))

        # Listener for drum machine preview button
        for i in range(self.__number_of_drum_machine_channels):
            dmc = self.__drum_machine_channels_list[i]
            dmc_index = dmc.channel_id
            btn = dmc.preview_button
            btn.released.connect(lambda dmc_i=dmc_index: self.__play_preview(dmc_i))

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

        #####################################################################################################
        ########################## Listeners for Transport module ################################
        #####################################################################################################

        # Listeners for Transport module
        self.__transport.btn_play.clicked.connect(lambda: self.start_playback())
        self.__transport.btn_stop.clicked.connect(lambda: self.stop_playback())
        self.__transport.tempo_spinbox.valueChanged.connect(lambda value: self.set_tempo(value))
        self.__transport.metronome_checkbox.clicked.connect(
            lambda checked: self.set_metronome_on_off(checked)
        )

        #####################################################################################################
        ########################## Listeners for Timing resolution module ################################
        #####################################################################################################

        # Listener for Timing resolution module
        self.__sequencer_module.timing_resolution_select. \
            timing_select_dial.valueChanged.connect(lambda index: self.set_timing_resolution(index))

    ########################################################################
    # Take action upon receiving pulse from app_timer
    ########################################################################
    def on_pulse(self, count):
        print(f"DrumMachine received pulse {count}")
        # Trigger sound playback or other logic here
        self.__sequencer_module.stepper.play_step_color(count)
        self.__sequencer_module.stepper.stepper_indicators_on_play(count)

        # self.__drum_machine_channels_list[self.__current_selected_drum_machine_channel_index].play_sample()

    # start playback
    def start_playback(self):
        self.__app_timer.start_counter()

    # stop playback
    def stop_playback(self):
        self.__app_timer.stop_counter()
        self.__sequencer_module.stepper.current_stepper_buttons_selected(self.__current_pattern)
        self.__sequencer_module.stepper.reset_stepper_indicators()

    def set_tempo(self, value):
        self.__app_timer.set_tempo(int(value))

    def set_metronome_on_off(self, is_on):
        self.__metronome_on = is_on
        print(f"metronome: {self.__metronome_on}")

    def set_time_resolution(self, bpb, meter):
        self.__app_timer.set_timing_resolution(bpb, meter)

    def set_timing_resolution(self, index):
        index = index - 1
        self.set_time_resolution(self.__timing_resolution_dict[index][0], self.__timing_resolution_dict[index][1])

    def __update_bank_index(self, index):
        self.__bank_index = index
        self.__global_pattern_bank_index = self.__bank_index
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
        self.__current_pattern = self.__pattern_manager.bank_dict[self.__bank_index][self.__global_pattern_bank_index][
            self.__channel_pattern_index]
        self.__update_stepper_display()

    def __update_stepper_display(self):
        print(f'{self.__global_pattern_bank_index}{self.__global_pattern_index}{self.__channel_pattern_index}')
        self.__sequencer_module.stepper.current_stepper_buttons_selected(
            self.__pattern_manager.bank_dict[self.__global_pattern_bank_index][self.__global_pattern_index][
                self.__channel_pattern_index])

    def __play_preview(self, index):
        print(f"preview {index}")
        self.__audio_channels_list[index].voice.preview_voice()

    def __set_voice_for_drum_machine_channels(self, index, dmc_index):
        voice = AudioVoice(self.__samples_dir + f"\\{self.__audio_samples_list[index].name}")
        self.__audio_channels_list[dmc_index].voice = voice
        print(f'voice: {voice} for channel: {dmc_index}')

    def __set_channel_volume(self, index, value):
        self.__audio_channels_list[index].volume = value / 100

    def __set_channel_pan(self, index, value):
        self.__audio_channels_list[index].pan = value / 100

    def __set_sample_length(self, index, value):
        print(f"{self.__audio_channels_list[index]} : value")
        self.__audio_channels_list[index].voice.set_sample_length(value)

    def __set_sample_pitch(self, index, value):
        print(f"{self.__audio_channels_list[index]} : value")
        self.__audio_channels_list[index].voice.modify_sample_rate(value)

    def __set_sample_duration(self, index, value):
        print(f"{self.__audio_channels_list[index]} : value")
        self.__audio_channels_list[index].voice.set_sample_duration(value)

    ####################################################
    ## Create a list of sounds from dir
    ####################################################
    def get_audio_samples_list(self):
        print(f"debug: {self.__samples_dir}")
        directory = Path(self.__samples_dir)

        # mode = os.stat(self.__samples_dir).st_mode
        # print("Is directory:", stat.S_ISDIR(mode))
        # print("Is readable:", os.access(self.__samples_dir, os.R_OK))
        # print("Is writable:", os.access(self.__samples_dir, os.W_OK))

        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a valid directory!")

        audio_list = []
        try:
            for file in directory.iterdir():
                print(f"checking file: {file}")
                if file.is_file():
                    audio_list.append(file)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error when scanning directory: {e}")

        return audio_list
