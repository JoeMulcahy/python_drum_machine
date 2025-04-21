from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QMainWindow, QVBoxLayout

from Channel import Channel
from sequencer_module.SequencerModule import SequencerModule
from transport_module.Transport import Transport


class DrumMachine(QWidget):
    def __init__(self):
        super().__init__()
        drum_machine_layout = QGridLayout()  # layout for various modules in drum machine
        self.__init_number_of_steps = 16  # initial number of steps in stepper
        self.__current_global_pattern = 1  # pattern select (PatternSelect.py)

        self.__channels_list = list()  # list of channel modules
        self.__stepper_patterns_for_channels_list = list()  # list of stepper patterns for each channel
        self.__global_stepper_patterns_dict = dict()  # dictionary of global patterns

        # layout for the step sequencer's audio channels
        channels_layout = QGridLayout()
        channels_layout.setSpacing(15)
        channels_layout.setContentsMargins(10, 10, 10, 10)

        # layout for transport, step sequencer modules
        controls_layout = QGridLayout()
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(10, 10, 10, 10)

        # create 8 channels and to layout
        # initialise stepper patterns for each channel and add to stepper_patterns_for_channels_list
        # add channel to channels layout
        for i in range(8):
            channel = Channel(i)
            self.__channels_list.append(channel)
            self.__stepper_patterns_for_channels_list.append([0 for i in range(self.__init_number_of_steps)])
            channels_layout.addWidget(channel, 0, i)

        self.__current_pattern = self.__stepper_patterns_for_channels_list[0]

        # new Transport and SequencerModule
        self.__transport = Transport()
        self.__sequencer_module = SequencerModule(self.__init_number_of_steps)

        # create dictionary of global stepper patterns from all channels
        for i in range(self.__sequencer_module.pattern_select.number_of_buttons):
            self.__global_stepper_patterns_dict[i] = self.__stepper_patterns_for_channels_list

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

    # highlight channel upon selection
    # select pattern associated with selected channel and update pattern on the stepper
    def select_channel(self, btn_id):
        for channel in self.__channels_list:
            channel.unselect_channel()

        channel = self.__channels_list[int(btn_id)]
        channel.select_channel()
        self.__current_pattern = self.__stepper_patterns_for_channels_list[int(btn_id)]
        self.__sequencer_module.stepper.current_stepper_buttons_selected(self.__current_pattern)
