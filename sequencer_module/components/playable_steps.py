from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QSpinBox


class PlayableSteps(QWidget):
    def __init__(self, number_of_steps):
        super().__init__()
        self.__number_of_steps = number_of_steps
        self.__current_number_of_playable_steps = number_of_steps
        self.__steps_spin_box = QSpinBox()

        self.group_box_step_select = QGroupBox("Steps")
        self.steps_select_layout = QGridLayout()

        # step spin box
        self.__steps_spin_box.setRange(1, self.__number_of_steps)
        self.__steps_spin_box.setValue(self.__number_of_steps)
        self.steps_select_layout.addWidget(self.__steps_spin_box, 0, 0)

        self.group_box_step_select.setLayout(self.steps_select_layout)
        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_step_select)
        self.setLayout(main_layout)

    def set_spinbox_range(self, value):
        self.__steps_spin_box.setRange(1, value)

    def set_spinbox_value(self, value):
        self.__steps_spin_box.setValue(value)

    @property
    def current_number_of_playable_steps(self):
        return self.__current_number_of_playable_steps

    @property
    def playable_steps_spinbox(self):
        return self.__steps_spin_box


