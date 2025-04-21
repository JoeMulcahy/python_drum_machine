from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QDial


#   TimingSelector
#   - Selects a timing value which represents the number of beats in a bar

class TimingSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.__current_index = 2

        self.group_box_time_resolution_select = QGroupBox("Timing")
        self.timing_select_layout = QGridLayout()

        self.timing_select_dial = QDial()
        self.timing_select_values_list = ("1/2", "1/4", "1/8", "1/8T", "1/16", "1/16T", "1/32", "1/64")
        self.timing_select_label = QLabel(self.timing_select_values_list[self.__current_index])

        self.timing_select_dial.setFixedSize(50, 50)
        self.timing_select_dial.setRange(1, 8)
        self.timing_select_dial.setValue(3)
        self.timing_select_dial.setSingleStep(1)
        self.timing_select_dial.setPageStep(1)
        self.timing_select_dial.setNotchesVisible(True)
        self.timing_select_dial.setWrapping(False)

        self.timing_select_layout.addWidget(self.timing_select_dial, 0, 0)
        self.timing_select_layout.addWidget(self.timing_select_label, 0, 1)

        self.group_box_time_resolution_select.setLayout(self.timing_select_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_time_resolution_select)
        self.setLayout(main_layout)

        # Listeners
        self.timing_select_dial.valueChanged.connect(lambda: self.set_timing_label())

    @property
    def current_index(self):
        return self.__current_index

    def set_timing_label(self):
        print(self.timing_select_values_list[self.timing_select_dial.value() - 1])
        self.timing_select_label.setText(self.timing_select_values_list[self.timing_select_dial.value() - 1])

    @current_index.setter
    def current_index(self, value):
        self.__current_index = value
