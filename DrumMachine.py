import random
from zipfile import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QMainWindow, QVBoxLayout

from Drum_Machine_Channel import DrumMachineChannel
from sequencer_module.SequencerModule import SequencerModule
from sound_engine import AudioVoice, Channel
from sound_engine.SoundEngine import SoundEngine
from sound_engine.SoundWave import SoundWave, SinWave

from timer.ApplicationTimer import ApplicationTimer
from transport_module.Transport import Transport


class DrumMachine(QWidget):
    def __init__(self):
        super().__init__()
        drum_machine_layout = QGridLayout()                 # layout for various modules in drum machine
        self.__init_number_of_steps = 16                    # initial number of steps in stepper
        self.__current_global_pattern = list()              # pattern select (PatternSelect.py)

        self.__channels_list = list()                       # list of channel modules
        self.__stepper_patterns_for_channels_list = list()  # list of stepper patterns for each channel
        self.__global_stepper_patterns_dict = dict()        # dictionary of global patterns
        self.__current_pattern_button_index = 0
        self.__current_selected_channel_index = 0

        self.__tempo = 120
        self.__beats_per_bar = 4
        self.__meter = 4

        self.__timing_resolution_dict = self.create_timing_resolution_dict()    # dictionary of [bpm, meter] timings

        self.__metronome_on = False                                             # metronome on/off flag

        audio_engine = SoundEngine()
        self.samples_dir = r"C:\Users\josep\Desktop\Step Seq\audio"
        self.audio_samples_list = self.get_audio_samples_list()
        self.audio_sample_names = [file.name for file in self.audio_samples_list]


        # initialise application timer
        self.__app_timer = ApplicationTimer(120, 4, 4)
        self.__app_timer.set_pulse_callback(self.on_pulse)                      # receive a 'pulse' from app_timer

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
        # initialise stepper patterns for each channel and add to stepper_patterns_for_channels_list
        # add channel to channels layout
        for i in range(8):
            dm_channel = DrumMachineChannel(i)
            audio_voice = AudioVoice(self.samples_dir + f"\\{self.audio_samples_list[0].name}")
            audio_channel = Channel(audio_voice, volume=0.5, pan=0.5)
            audio_engine.add_channel(audio_channel)
            self.__channels_list.append(dm_channel)
            self.__stepper_patterns_for_channels_list.append([0 for i in range(self.__init_number_of_steps)])
            channels_layout.addWidget(dm_channel, 0, i)

        # new Transport and SequencerModule
        self.__transport = Transport()
        self.__sequencer_module = SequencerModule(self.__init_number_of_steps)

        # create dictionary of global stepper patterns from all channels
        for i in range(self.__sequencer_module.pattern_select.number_of_buttons):
            self.__global_stepper_patterns_dict[i] = self.initialise_pattern()

        self.__current_global_pattern = self.__global_stepper_patterns_dict[self.__current_pattern_button_index]
        self.__current_pattern = self.__current_global_pattern[0]

        # select first channel as default
        self.select_channel(self.__current_selected_channel_index)

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

        # Listeners for channel select
        for channel in self.__channels_list:
            select_button = channel.select_button
            select_button.clicked.connect((lambda checked, b=select_button: self.select_channel(b.property("id"))))

        # Listener for (global) pattern select
        for btn in self.__sequencer_module.pattern_select.buttons_list:
            btn.clicked.connect(lambda checked, b=btn: self.__update_global_pattern(int(b.text())))

        # Listeners for Transport module
        self.__transport.btn_play.clicked.connect(lambda: self.start_playback())
        self.__transport.btn_stop.clicked.connect(lambda: self.stop_playback())
        self.__transport.tempo_spinbox.valueChanged.connect(lambda value: self.set_tempo(value))
        self.__transport.metronome_checkbox.clicked.connect(
            lambda checked: self.set_metronome_on_off(checked)
        )

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

        print(self.__current_pattern)
        if self.__current_pattern[count % 16] == 1:
            self.__channels_list[self.__current_selected_channel_index].play_sample()


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

    # highlight channel upon selection
    # select pattern associated with selected channel and update pattern on the stepper
    def select_channel(self, btn_id):
        self.__current_selected_channel_index = int(btn_id)
        for channel in self.__channels_list:
            channel.unselect_channel()

        channel = self.__channels_list[self.__current_selected_channel_index]
        channel.select_channel()

        self.__current_pattern = self.__global_stepper_patterns_dict[self.__current_pattern_button_index][
            self.__current_selected_channel_index]
        self.__sequencer_module.stepper.current_stepper_buttons_selected(self.__current_pattern)

    def __update_global_pattern(self, index):
        self.__current_global_pattern = self.__global_stepper_patterns_dict[index - 1]
        self.__current_pattern = self.__current_global_pattern[self.__current_selected_channel_index]
        self.__sequencer_module.stepper.current_stepper_buttons_selected(self.__current_pattern)

        print("Debug")
        print(f"index: {index - 1}")
        print(f"channel index: {self.__current_selected_channel_index}")
        print(f"")

    def initialise_pattern(self):
        patterns_list = list()
        for i in range(self.__sequencer_module.pattern_select.number_of_buttons):
            patterns_list.append([0 for i in range(self.__init_number_of_steps)])

        return patterns_list

    def create_timing_resolution_dict(self):
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
