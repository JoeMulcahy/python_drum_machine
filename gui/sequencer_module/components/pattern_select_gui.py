from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton, QSizePolicy

import settings


class PatternSelect(QWidget):
    def __init__(self, number_of_buttons, number_of_banks):
        super().__init__()

        self.__buttons_list = list()
        self.__bank_buttons_list = list()
        self.__selected_button_index = 0
        self.__selected_bank_index = 0
        self.__number_of_button = number_of_buttons
        self.__number_of_banks = number_of_banks
        bank_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        self.pattern_select_layout = QGridLayout()
        self.group_box_pattern_select = QGroupBox("Pattern")

        # pattern select buttons
        for i in range(number_of_buttons):
            button = QPushButton(f"{i + 1}")
            button.setFixedSize(40, 30)
            button.setSizePolicy(settings.FIXED_SIZE_POLICY)
            button.setStyleSheet(settings.PATTERN_BUTTON_DEFAULT_STYLING)
            self.__buttons_list.append(button)
            self.pattern_select_layout.addWidget(button, int(i / 4), i % 4, 1, 1, Qt.AlignmentFlag.AlignCenter)
            self.__buttons_list[0].setStyleSheet(settings.PATTERN_BUTTON_ON_STYLING)

        for i in range(self.__number_of_banks):
            button = QPushButton(f"{bank_letters[i]}")
            button.setFixedSize(40, 30)
            button.setSizePolicy(settings.FIXED_SIZE_POLICY)
            button.setStyleSheet(settings.BANK_BUTTON_DEFAULT_STYLING)
            self.__bank_buttons_list.append(button)
            self.pattern_select_layout.addWidget(button, 2, i, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.__bank_buttons_list[0].setStyleSheet(settings.BANK_BUTTON_ON_STYLING)

        self.__btn_copy = QPushButton('Copy')
        self.__btn_paste = QPushButton('Paste')

        for button in [self.__btn_copy, self.__btn_paste]:
            button.setSizePolicy(settings.FIXED_SIZE_POLICY)
            button.setFixedSize(50, 30)
            button.setStyleSheet(settings.BUTTON_STYLE_1)

        self.pattern_select_layout.addWidget(self.__btn_copy, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.pattern_select_layout.addWidget(self.__btn_paste, 3, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Listener to set selected pattern button index and to highlight selected button
        for btn in self.__buttons_list:
            btn.clicked.connect(lambda checked, b=btn: self.set_button_index(b.text()))

        # Listener to set selected bank button index and to highlight selected bank button
        for i in range(self.__number_of_banks):
            btn = self.__bank_buttons_list[i]
            btn.clicked.connect(lambda checked, index=i: self.set_bank_index(index))

        self.group_box_pattern_select.setLayout(self.pattern_select_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_pattern_select)
        self.setLayout(main_layout)

    def set_button_index(self, value):
        self.__selected_button_index = int(value) - 1
        self.__update_pattern_select_buttons_visually(self.__selected_button_index)

    def set_bank_index(self, index):
        print(f'debug: bank index: {index}')
        self.__selected_bank_index = index
        self.__update_bank_select_buttons_visually(index)

    @property
    def buttons_list(self):
        return self.__buttons_list

    @property
    def bank_buttons_list(self):
        return self.__bank_buttons_list

    @property
    def copy_button(self):
        return self.__btn_copy

    @property
    def paste_button(self):
        return self.__btn_paste

    @property
    def selected_button_index(self):
        return self.__selected_button_index

    @property
    def selected_bank_index(self):
        return self.__selected_bank_index

    @property
    def number_of_buttons(self):
        return self.__number_of_button

    @selected_button_index.setter
    def selected_button_index(self, value):
        self.__selected_button_index = value
        self.__update_pattern_select_buttons_visually(value)

    @selected_bank_index.setter
    def selected_bank_index(self, value):
        self.__selected_bank_index = value
        self.__update_bank_select_buttons_visually(value)

    def __update_pattern_select_buttons_visually(self, index):
        for x in range(self.__number_of_button):
            self.__buttons_list[x].setStyleSheet(self.default_color)
            if self.__selected_button_index == index:
                self.__buttons_list[index].setStyleSheet(self.toggle_on_color)

    def __update_bank_select_buttons_visually(self, index):
        for x in range(self.__number_of_banks):
            self.__bank_buttons_list[x].setStyleSheet(self.default_color_bank)
            if self.__selected_bank_index == index:
                self.__bank_buttons_list[index].setStyleSheet(self.toggle_on_color_bank)
