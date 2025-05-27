from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QVBoxLayout

import settings
from gui.sequencer_module.components.playable_steps_gui import PlayableSteps
from gui.sequencer_module.components.pattern_select_gui import PatternSelect
from gui.sequencer_module.components.stepper_gui import Stepper
from gui.sequencer_module.components.beat_timing_gui import TimingSelector


class SequencerModule(QWidget):
    def __init__(self, initial_number_of_steps):
        super().__init__()

        self.__timing_resolution_select = TimingSelector()
        self.__stepper = Stepper(1, initial_number_of_steps)
        self.__pattern_select = PatternSelect(8, 4)
        self.__playable_steps_module = PlayableSteps(16)

        stepper_module_layout = QGridLayout()
        group_box_stepper_module = QGroupBox("Sequencer")
        group_box_stepper_module.setSizePolicy(settings.FIXED_SIZE_POLICY)

        stepper_module_layout.addWidget(self.__pattern_select, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        stepper_module_layout.addWidget(self.__playable_steps_module, 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        stepper_module_layout.addWidget(self.__timing_resolution_select, 0, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        stepper_module_layout.addWidget(self.__stepper, 2, 0, 1, 3)

        group_box_stepper_module.setLayout(stepper_module_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box_stepper_module, 0, 0)
        self.setLayout(main_layout)

    @property
    def stepper(self):
        return self.__stepper

    @property
    def timing_resolution_select(self):
        return self.__timing_resolution_select

    @property
    def playable_steps_module(self):
        return self.__playable_steps_module

    @property
    def pattern_select(self):
        return self.__pattern_select



