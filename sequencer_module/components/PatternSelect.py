from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton


class PatternSelect(QWidget):
    def __init__(self, number_of_buttons):
        super().__init__()

        self.__buttons_list = list()
        self.__selected_button_index = 0
        self.__number_of_button = number_of_buttons

        self.pattern_select_layout = QGridLayout()
        self.group_box_pattern_select = QGroupBox("Pattern")

        # colors
        self.default_color = "background-color: #3498db; color: white;"
        self.toggle_on_color = "background-color: #9999ef; color: white;"

        # pattern select buttons
        for i in range(number_of_buttons):
            button = QPushButton(f"{i + 1}")
            button.setFixedSize(30, 30)
            button.setStyleSheet(self.default_color)
            self.__buttons_list.append(button)

            self.pattern_select_layout.addWidget(button, int(i / 3), i % 3)
            self.__buttons_list[0].setStyleSheet(self.toggle_on_color)

        # Listener
        for btn in self.__buttons_list:
            btn.clicked.connect(lambda checked, b=btn: self.set_button_index(b.text()))

        self.group_box_pattern_select.setLayout(self.pattern_select_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_pattern_select)
        self.setLayout(main_layout)

    def set_button_index(self, value):
        self.__selected_button_index = int(value) - 1
        self.__update_pattern_select_buttons_visually(self.__selected_button_index)

    @property
    def selected_button_index(self):
        return self.__selected_button_index

    @property
    def number_of_buttons(self):
        return self.__number_of_button

    @selected_button_index.setter
    def selected_button_index(self, value):
        self.__selected_button_index = value
        self.__update_pattern_select_buttons_visually(value)

    def __update_pattern_select_buttons_visually(self, index):
        for x in range(self.__number_of_button):
            self.__buttons_list[x].setStyleSheet(self.default_color)
            if self.__selected_button_index == index:
                self.__buttons_list[index].setStyleSheet(self.toggle_on_color)


