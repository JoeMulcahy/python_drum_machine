from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QDial

#   TimingSelector
#   - Selects a timing value which represents the number of beats in a bar
import settings


class TimingSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.__current_index = 4

        self.group_box_time_resolution_select = QGroupBox("Timing")
        self.group_box_time_resolution_select.setStyleSheet(settings.GROUPBOX_STYLE_1)
        self.timing_select_layout = QGridLayout()
        self.timing_select_layout.setSpacing(5)

        self.timing_select_dial = QDial()
        self.timing_select_values_list = ("1/2", "1/4", "1/8", "1/8T", "1/16", "1/16T", "1/32", "1/64")
        self.timing_select_label = QLabel(self.timing_select_values_list[self.__current_index])

        self.timing_select_dial.setFixedSize(50, 50)
        self.timing_select_dial.setRange(1, 8)
        self.timing_select_dial.setValue(self.__current_index + 1)
        self.timing_select_dial.setSingleStep(1)
        self.timing_select_dial.setPageStep(1)
        self.timing_select_dial.setNotchesVisible(True)
        self.timing_select_dial.setWrapping(False)

        self.__flam_dial = QDial()
        self.__swing_dial = QDial()
        self.__humanise_dial = QDial()

        for dial in [self.__flam_dial, self.__swing_dial, self.__humanise_dial]:
            dial.setFixedSize(35, 35)
            dial.setSizePolicy(settings.FIXED_SIZE_POLICY)
            dial.setRange(0, 100)
            dial.setValue(0)
            dial.setNotchesVisible(True)

        self.__lbl_flam = QLabel('Flam')
        self.__lbl_swing = QLabel('Swing')
        self.__lbl_humanise = QLabel('Humanise')

        for lbl in [self.__lbl_flam, self.__lbl_swing, self.__lbl_humanise]:
            lbl.setStyleSheet(settings.LABEL_STYLE_2)

        self.timing_select_layout.addWidget(self.timing_select_dial, 0, 0, 1, 2)
        self.timing_select_layout.addWidget(self.timing_select_label, 0, 2, 1, 1)

        self.timing_select_layout.addWidget(self.__flam_dial, 1, 0, 1, 1)
        self.timing_select_layout.addWidget(self.__swing_dial, 1, 1, 1, 1)
        self.timing_select_layout.addWidget(self.__humanise_dial, 1, 2, 1, 1)

        self.timing_select_layout.addWidget(self.__lbl_flam, 2, 0, 1, 1)
        self.timing_select_layout.addWidget(self.__lbl_swing, 2, 1, 1, 1)
        self.timing_select_layout.addWidget(self.__lbl_humanise, 2, 2, 1, 1)

        self.group_box_time_resolution_select.setLayout(self.timing_select_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(self.group_box_time_resolution_select)
        self.setLayout(main_layout)

        # Listeners - set timing label
        self.timing_select_dial.valueChanged.connect(lambda: self.set_timing_label())

    @property
    def current_index(self):
        return self.__current_index

    def set_timing_label(self):
        print(self.timing_select_values_list[self.timing_select_dial.value() - 1])
        self.__current_index = self.timing_select_dial.value() - 1
        self.timing_select_label.setText(self.timing_select_values_list[self.__current_index])

    @current_index.setter
    def current_index(self, value):
        self.__current_index = value

    @property
    def flam_dial(self):
        return self.__flam_dial

    @property
    def swing_dial(self):
        return self.__swing_dial

    @property
    def humanise_dial(self):
        return self.__humanise_dial
