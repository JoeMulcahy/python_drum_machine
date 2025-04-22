from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QGroupBox, QLabel


class Stepper(QWidget):
    def __init__(self, stepper_id, number_of_steps):
        super().__init__()

        self.__stepper_id = stepper_id
        self.__stepper_buttons_list = list()
        self.__current_stepper_buttons_selected = [0 for x in range(number_of_steps)]
        self.__number_of_steps = number_of_steps
        self.__number_of_steps_playable = self.__number_of_steps

        self.group_box_stepper = QGroupBox("Stepper")

        self.stepper_layout = QGridLayout()

        # button colors
        self.default_color = "background-color: #3498db; color: white;"
        self.toggle_on_color = "background-color: #ef9912; color: white;"
        self.play_color = "background-color: #12ff12; color: white;"

        # stepper buttons
        for i in range(self.__number_of_steps):
            step_indicator = QLabel(f".")
            step_indicator.setStyleSheet(
                """
                    QLabel {
                        font-size: 40px;       /* Resize text */
                        color: #12ff12;        /* Change text color */
                    }
                """
            )
            button = QPushButton()
            button.setProperty("id", i)
            button.setFixedSize(50, 50)
            button.setStyleSheet(self.default_color)  # set color
            label = QLabel(f"{i + 1}")
            self.__stepper_buttons_list.append(button)
            self.stepper_layout.addWidget(step_indicator, 0, int(i), alignment=Qt.AlignmentFlag.AlignHCenter)
            self.stepper_layout.addWidget(button, 1, int(i), alignment=Qt.AlignmentFlag.AlignBottom)
            self.stepper_layout.addWidget(label, 2, int(i), alignment=Qt.AlignmentFlag.AlignHCenter)
            self.stepper_layout.setRowStretch(0, 5)
            self.stepper_layout.setRowStretch(1, 1)

        # Listeners
        for btn in self.__stepper_buttons_list:
            btn.clicked.connect(lambda checked, b=btn: self.__button_toggle(b.property("id")))

        self.group_box_stepper.setLayout(self.stepper_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_stepper)
        self.setLayout(main_layout)

    def __button_toggle(self, btn_id):
        self.__update_stepper_buttons_list(int(btn_id))

    def __update_stepper_buttons_list(self, index):
        if self.__current_stepper_buttons_selected[index] == 0:
            self.__current_stepper_buttons_selected[index] = 1
        else:
            self.__current_stepper_buttons_selected[index] = 0
        #print(self.__current_stepper_buttons_selected)
        self.__update_stepper_button_pattern_visually()

    def __update_stepper_button_pattern_visually(self):
        for i in range(len(self.__current_stepper_buttons_selected)):
            if self.__current_stepper_buttons_selected[i] == 1:
                self.__stepper_buttons_list[i].setStyleSheet(self.toggle_on_color)
            elif self.__current_stepper_buttons_selected[i] == 0:
                self.__stepper_buttons_list[i].setStyleSheet(self.default_color)

    @property
    def current_stepper_buttons_selected(self):
        return self.__current_stepper_buttons_selected

    def current_stepper_buttons_selected(self, values_array):
        self.__current_stepper_buttons_selected = values_array
        self.__update_stepper_button_pattern_visually()

    def show_stepper(self):
        self.setVisible(True)

    def hide_stepper(self):
        self.setVisible(False)

    @property
    def stepper_id(self):
        return self.__stepper_id

    @property
    def number_of_steps(self):
        return self.__number_of_steps

    @property
    def number_of_steps_playable(self):
        return self.__number_of_steps_playable

    @number_of_steps.setter
    def number_of_steps(self, value):
        self.__number_of_steps = value

    def __play_step_color(self, index):
        previous_index = (index - 1) % self.__number_of_steps
        self.__stepper_buttons_list[index].setStyleSheet(self.play_color)
        if self.__current_stepper_buttons_selected[previous_index] == 1:
            self.__stepper_buttons_list[previous_index].setStyleSheet(self.toggle_on_color)
        elif self.__current_stepper_buttons_selected[index] == 0:
            self.__stepper_buttons_list[previous_index].setStyleSheet(self.default_color)
