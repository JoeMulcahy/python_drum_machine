from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QSpinBox, QCheckBox, QPushButton

import settings


class PlayableSteps(QWidget):
    # might need a signal to change number of steps

    def __init__(self, number_of_steps):
        super().__init__()
        self.__number_of_steps = number_of_steps
        self.__current_number_of_playable_steps = number_of_steps
        self.__steps_spin_box = QSpinBox()

        self.__playable_steps_index = 0

        self.group_box_step_select = QGroupBox("Steps")
        self.steps_select_layout = QGridLayout()

        # step spin box
        self.__steps_spin_box.setRange(1, self.__number_of_steps)
        self.__steps_spin_box.setValue(self.__number_of_steps)
        self.steps_select_layout.addWidget(self.__steps_spin_box, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)

        self.__lbl_steps_1_16 = QLabel('1 - 16')
        self.__lbl_steps_17_32 = QLabel('17 - 32')
        self.__lbl_steps_33_48 = QLabel('33 - 48')
        self.__lbl_steps_49_64 = QLabel('49 - 64')

        self.__buttons_list = []
        self.__btn_1_16 = QPushButton()
        self.__btn_17_32 = QPushButton()
        self.__btn_33_48 = QPushButton()
        self.__btn_49_64 = QPushButton()
        self.__buttons_list.append(self.__btn_1_16)
        self.__buttons_list.append(self.__btn_17_32)
        self.__buttons_list.append(self.__btn_33_48)
        self.__buttons_list.append(self.__btn_49_64)

        self.__buttons_list[0].setChecked(True)

        self.steps_select_layout.addWidget(self.__btn_1_16, 1, 0, 1, 1)
        self.steps_select_layout.addWidget(self.__lbl_steps_1_16, 1, 1, 1, 1)
        self.steps_select_layout.addWidget(self.__btn_17_32, 2, 0, 1, 1)
        self.steps_select_layout.addWidget(self.__lbl_steps_17_32, 2, 1, 1, 1)
        self.steps_select_layout.addWidget(self.__btn_33_48, 3, 0, 1, 1)
        self.steps_select_layout.addWidget(self.__lbl_steps_33_48, 3, 1, 1, 1)
        self.steps_select_layout.addWidget(self.__btn_49_64, 4, 0, 1, 1)
        self.steps_select_layout.addWidget(self.__lbl_steps_49_64, 4, 1, 1, 1)

        for i, btn in enumerate(self.__buttons_list):
            btn.pressed.connect(lambda index=i: self.__select_button(index))

        self.__select_button(0)

        self.__set_style()

        self.group_box_step_select.setLayout(self.steps_select_layout)
        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_step_select)
        self.setLayout(main_layout)

    def update_max_playable_steps(self, value):
        self.__number_of_steps = value
        self.__steps_spin_box.setRange(1, self.__number_of_steps)
        self.__steps_spin_box.setValue(self.__number_of_steps)

    def __select_button(self, index):
        for btn in self.__buttons_list:
            btn.setStyleSheet(settings.STEPPER_BUTTON_DEFAULT_STYLING)

        self.__buttons_list[index].setStyleSheet(settings.STEPPER_BUTTON_ON_STYLING)

    def __set_style(self):
        self.__steps_spin_box.setStyleSheet(settings.TEMPO_SPINBOX_STYLE)

        for lbl in [self.__lbl_steps_1_16, self.__lbl_steps_17_32, self.__lbl_steps_33_48, self.__lbl_steps_49_64]:
            lbl.setStyleSheet(settings.LABEL_STYLE_2)

        for cb in self.__buttons_list:
            cb.setFixedSize(20, 20)
            cb.setSizePolicy(settings.FIXED_SIZE_POLICY)
            # self.setStyleSheet(settings.CHECKBOX_STYLE_1)

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

    @property
    def playable_steps_index(self):
        return self.__playable_steps_index

    @playable_steps_index.setter
    def playable_steps_index(self, value):
        self.__playable_steps_index = value

    @property
    def steps_button_1_16(self):
        return self.__btn_1_16

    @property
    def steps_button_17_32(self):
        return self.__btn_17_32

    @property
    def steps_button_33_48(self):
        return self.__btn_33_48

    @property
    def steps_button_49_64(self):
        return self.__btn_49_64

    @property
    def steps_label_1_16(self):
        return self.__lbl_steps_1_16

    @property
    def steps_label_17_32(self):
        return self.__lbl_steps_17_32

    @property
    def steps_label_33_48(self):
        return self.__lbl_steps_33_48

    @property
    def steps_label_49_64(self):
        return self.__lbl_steps_49_64


