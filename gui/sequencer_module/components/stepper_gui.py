from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QGroupBox, QLabel, QComboBox, QSpinBox, QSizePolicy

import settings
from signals import DrumMachineSignals


class Stepper(QWidget):
    def __init__(self, stepper_id, number_of_steps):
        super().__init__()

        self.__stepper_id = stepper_id
        self.__stepper_buttons_list = list()
        self.__current_stepper_buttons_selected = [0 for x in range(number_of_steps)]
        self.__number_of_steps = number_of_steps
        self.__number_of_steps_playable = self.__number_of_steps
        self.__step_indicator_list = list()  # list of stepper indicator (above stepper buttons)

        self.group_box_stepper = QGroupBox("Stepper")
        self.stepper_layout = QGridLayout()

        # labels
        self.__lbl_shift = QLabel('Shift')
        self.__lbl_generate_pattern = QLabel("Generate")

        # stepper controls
        self.__btn_shift_left = QPushButton()
        self.__btn_shift_right = QPushButton()
        self.__btn_clear_pattern = QPushButton("clear")
        self.__btn_invert_pattern = QPushButton("invert")

        self.__btn_generate_pattern = QPushButton()
        self.__spin_step_freq = QSpinBox()
        self.__spin_step_freq.setRange(1, int(self.__number_of_steps - 1))
        self.__spin_step_freq.setValue(4)

        self.__btn_generate_random = QPushButton()

        self.__btn_copy_pattern = QPushButton("Copy")
        self.__btn_paste_pattern = QPushButton("Paste")

        self.__btn_shift_left.setIcon(QIcon("images/left-chevron.png"))
        self.__btn_shift_right.setIcon(QIcon("images/right-chevron.png"))
        self.__btn_generate_random.setIcon(QIcon("images/dices.png"))

        self.stepper_layout.addWidget(self.__lbl_shift, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.stepper_layout.addWidget(self.__btn_shift_left, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stepper_layout.addWidget(self.__btn_shift_right, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stepper_layout.addWidget(self.__btn_clear_pattern, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stepper_layout.addWidget(self.__btn_invert_pattern, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.stepper_layout.addWidget(self.__lbl_generate_pattern, 0, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.stepper_layout.addWidget(self.__btn_generate_pattern, 0, 7, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stepper_layout.addWidget(self.__spin_step_freq, 0, 8, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stepper_layout.addWidget(self.__btn_generate_random, 0, 9, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.stepper_layout.addWidget(self.__btn_copy_pattern, 0, 11, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.stepper_layout.addWidget(self.__btn_paste_pattern, 0, 12, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        for i in range(self.__number_of_steps):
            step_indicator = QLabel(f".")
            step_indicator.setStyleSheet(settings.STEPPER_INDICATOR_DEFAULT_STYLING)
            step_indicator.setSizePolicy(settings.FIXED_SIZE_POLICY)
            self.__step_indicator_list.append(step_indicator)

            button = QPushButton()
            button.setSizePolicy(settings.FIXED_SIZE_POLICY)
            button.setProperty("id", i)
            button.setFixedSize(50, 50)
            button.setStyleSheet(settings.STEPPER_BUTTON_DEFAULT_STYLING)  # set color

            label = QLabel(f"{i + 1}")
            self.__stepper_buttons_list.append(button)
            self.stepper_layout.addWidget(step_indicator, 1, int(i), alignment=Qt.AlignmentFlag.AlignHCenter)
            self.stepper_layout.addWidget(button, 2, int(i), alignment=Qt.AlignmentFlag.AlignBottom)
            self.stepper_layout.addWidget(label, 3, int(i), alignment=Qt.AlignmentFlag.AlignHCenter)

        # Listeners
        for btn in self.__stepper_buttons_list:
            btn.clicked.connect(lambda checked, b=btn: self.__button_toggle(b.property("id")))

        self.__set_style()

        self.group_box_stepper.setLayout(self.stepper_layout)
        self.group_box_stepper.setSizePolicy(settings.FIXED_SIZE_POLICY)

        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_stepper)
        self.setLayout(main_layout)

    def __set_style(self):
        self.__lbl_shift.setStyleSheet(settings.LABEL_STYLE_1)

        for btn in [
            self.__btn_shift_left, self.__btn_shift_right, self.__btn_clear_pattern, self.__btn_invert_pattern,
            self.__btn_generate_pattern, self.__btn_generate_random, self.__btn_copy_pattern, self.__btn_paste_pattern
        ]:
            btn.setFixedSize(40, 20)
            btn.setSizePolicy(settings.FIXED_SIZE_POLICY)
            btn.setStyleSheet(settings.BUTTON_STYLE_1)

        self.__spin_step_freq.setStyleSheet(settings.STEP_FREQUENCY_SPINBOX_STYLING)
        self.__spin_step_freq.setFixedSize(40, 20)

    def __button_toggle(self, btn_id):
        self.__update_stepper_buttons_list(int(btn_id))

    def __update_stepper_buttons_list(self, index):
        if self.__current_stepper_buttons_selected[index] == 0:
            self.__current_stepper_buttons_selected[index] = 1
        else:
            self.__current_stepper_buttons_selected[index] = 0

        self.__update_stepper_button_pattern_visually()

    def __update_stepper_button_pattern_visually(self):
        for i in range(len(self.__current_stepper_buttons_selected)):
            if self.__current_stepper_buttons_selected[i] == 1:
                self.__stepper_buttons_list[i].setStyleSheet(settings.STEPPER_BUTTON_ON_STYLING)
            elif self.__current_stepper_buttons_selected[i] == 0:
                self.__stepper_buttons_list[i].setStyleSheet(settings.STEPPER_BUTTON_DEFAULT_STYLING)

    def current_stepper_buttons_selected(self, values_array):
        self.__current_stepper_buttons_selected = values_array
        self.__update_stepper_button_pattern_visually()

    def show_stepper(self):
        self.setVisible(True)

    def hide_stepper(self):
        self.setVisible(False)

    def play_step_color(self, index):
        index = index % self.__number_of_steps_playable
        previous_index = (index - 1) % self.__number_of_steps_playable  # ensures wrap-around

        self.__stepper_buttons_list[index].setStyleSheet(settings.STEPPER_BUTTON_PLAY_STYLING)

        if self.__current_stepper_buttons_selected[previous_index] == 1:
            self.__stepper_buttons_list[previous_index].setStyleSheet(settings.STEPPER_BUTTON_ON_STYLING)
        else:
            self.__stepper_buttons_list[previous_index].setStyleSheet(settings.STEPPER_BUTTON_DEFAULT_STYLING)

    def stepper_indicators_on_play(self, counter):
        counter = counter % self.__number_of_steps_playable
        self.__step_indicator_list[counter - 1].setStyleSheet(settings.STEPPER_INDICATOR_DEFAULT_STYLING)
        self.__step_indicator_list[counter].setStyleSheet(settings.STEPPER_INDICATOR_ON_STYLING)

    def reset_stepper_indicators(self):
        for indicator in self.__step_indicator_list:
            indicator.setStyleSheet(settings.STEPPER_INDICATOR_DEFAULT_STYLING)

    @property
    def stepper_id(self):
        return self.__stepper_id

    @property
    def number_of_steps(self):
        return self.__number_of_steps

    @property
    def number_of_playable_steps(self):
        return self.__number_of_steps_playable

    @number_of_playable_steps.setter
    def number_of_playable_steps(self, value):
        self.__number_of_steps_playable = value

    @number_of_steps.setter
    def number_of_steps(self, value):
        self.__number_of_steps = value

    @property
    def shift_left_button(self):
        return self.__btn_shift_left

    @property
    def shift_right_button(self):
        return self.__btn_shift_right

    @property
    def clear_button(self):
        return self.__btn_clear_pattern

    @property
    def generate_pattern_button(self):
        return self.__btn_generate_pattern

    @property
    def generate_random_pattern_button(self):
        return self.__btn_generate_random

    @property
    def invert_pattern_button(self):
        return self.__btn_invert_pattern

    @property
    def copy_button(self):
        return self.__btn_copy_pattern

    @property
    def paste_button(self):
        return self.__btn_paste_pattern

    @property
    def step_freq_spinbox(self):
        return self.__spin_step_freq
