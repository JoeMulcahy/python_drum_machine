from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QGroupBox, QVBoxLayout, QLabel, QDial, QSpinBox

from sequencer_module.components.TimingResolutionSelector import TimingSelector


class Stepper(QWidget):
    def __init__(self, number_of_steps):
        super().__init__()
        self.number_of_steps = number_of_steps

        self.stepper_buttons_list = list()
        self.pattern_select_buttons_list = list()

        self.timing_select_dial = QDial()
        self.timing_select_values_list = ("1/2", "1/4", "1/8", "1/8T", "1/16", "1/16T", "1/32", "1/64")
        self.timing_select_label = QLabel(self.timing_select_values_list[2])

        self.steps_spin_box = QSpinBox()

        self.group_box_sequencer_panel = QGroupBox(f"Sequencer")
        self.group_box_stepper = QGroupBox("Stepper")
        self.group_box_pattern_select = QGroupBox("Pattern")
        self.group_box_step_select = QGroupBox("Steps")
        self.group_box_time_resolution_select = QGroupBox("Timing")

        self.step_timing = 3
        self.initialise_components()

        # Listeners
        self.timing_select_dial.valueChanged.connect(lambda: self.set_timing_label())

    def initialise_components(self):
        stepper_layout = QGridLayout()
        pattern_select_layout = QGridLayout()
        steps_selection_layout = QGridLayout()
        timing_select_layout = QGridLayout()

        # stepper buttons
        for i in range(self.number_of_steps):
            button = QPushButton()
            button.setFixedSize(50, 50)
            label = QLabel(f"{i}")
            self.stepper_buttons_list.append(button)
            stepper_layout.addWidget(button, 0, int(i), alignment=Qt.AlignmentFlag.AlignBottom)
            stepper_layout.addWidget(label, 1, int(i), alignment=Qt.AlignmentFlag.AlignHCenter)
            stepper_layout.setRowStretch(0, 5)
            stepper_layout.setRowStretch(1, 1)

        # pattern select buttons
        for i in range(9):
            button = QPushButton(f"{i}")
            button.setFixedSize(30, 30)
            self.pattern_select_buttons_list.append(button)

            pattern_select_layout.addWidget(button, int(i / 3), i % 3)

        # step spin box
        self.steps_spin_box.setRange(1, 16)
        self.steps_spin_box.setValue(16)
        steps_selection_layout.addWidget(self.steps_spin_box, 0, 0)

        # timing dial
        self.timing_select_dial.setFixedSize(50, 50)
        self.timing_select_dial.setRange(1, 8)
        self.timing_select_dial.setSingleStep(1)
        self.timing_select_dial.setPageStep(1)
        self.timing_select_dial.setNotchesVisible(True)
        self.timing_select_dial.setWrapping(False)
        timing_select_layout.addWidget(self.timing_select_dial, 0, 0)
        timing_select_layout.addWidget(self.timing_select_label, 0, 1)

        sequencer_layout = QGridLayout()
        # sequencer_layout.addLayout(pattern_select_layout, 0, 0)
        # sequencer_layout.addLayout(steps_selection_layout, 0, 1)
        # sequencer_layout.addLayout(timing_select_layout, 0, 2)
        # sequencer_layout.addLayout(stepper_layout, 2, 1)

        self.group_box_pattern_select.setLayout(pattern_select_layout)
        # self.group_box_step_select(steps_selection_layout)
        # self.group_box_time_resolution_select(timing_select_layout)
        # self.group_box_stepper(timing_select_layout)

        sequencer_layout.addWidget(TimingSelector(), 0, 0)

        self.group_box_sequencer_panel.setLayout(sequencer_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.group_box_sequencer_panel)
        self.setLayout(main_layout)

        self.set_button_colors()

    def set_button_colors(self):
        for i in range(self.number_of_steps):
            if int(i / self.step_timing) % 2 == 0:
                self.stepper_buttons_list[i].setStyleSheet("background-color: #3498db; color: white;")
            else:
                self.stepper_buttons_list[i].setStyleSheet("background-color: #1212db; color: white;")

    def set_individual_button_color(self, index):
        self.stepper_buttons_list[index].setStyleSheet("background-color: #1212db; color: blue;")

    def set_timing_label(self):
        print(self.timing_select_values_list[self.timing_select_dial.value() - 1])
        self.timing_select_label.setText(self.timing_select_values_list[self.timing_select_dial.value() - 1])
