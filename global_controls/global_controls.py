from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QDial, QPushButton, QBoxLayout, QVBoxLayout, QGroupBox


class MasterControls(QWidget):
    def __init__(self):
        super().__init__()

        group_box = QGroupBox("Global Controls")
        controls_layout = QGridLayout()
        controls_layout.setSpacing(15)

        self.__lbl__volume = QLabel("Master Volume")
        self.__lbl__profile = QLabel("Profile")
        self.__lbl_un_solo_mute = QLabel("Reset")

        self.__volume_dial = QDial()
        self.__volume_dial.setFixedSize(70, 70)
        self.__volume_dial.setRange(0, 100)
        self.__volume_dial.setValue(50)
        self.__volume_dial.setWrapping(False)
        self.__volume_dial.setNotchesVisible(True)
        self.__btn_load_profile = QPushButton("Load")
        self.__btn_save_profile = QPushButton("Save")
        self.__btn_unmute_all = QPushButton("M")
        self.__btn_unsolo_all = QPushButton("S")

        controls_layout.addWidget(self.__lbl_un_solo_mute, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__btn_unsolo_all, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__btn_unmute_all, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        controls_layout.addWidget(self.__lbl__volume, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__volume_dial, 3, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        controls_layout.addWidget(self.__lbl__profile, 4, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__btn_load_profile, 5, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__btn_save_profile, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        button_style = "QPushButton { font-size: 10px; }"
        for btn in [self.__btn_load_profile, self.__btn_save_profile, self.__btn_unsolo_all, self.__btn_unmute_all]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(button_style)

        label_style = "QLabel { font-size: 12px; font-weight: bold; }"
        for lbl in [self.__lbl__volume, self.__lbl__profile, self.__lbl_un_solo_mute]:
            lbl.setStyleSheet(label_style)

        group_box.setLayout(controls_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    @property
    def volume_dial(self):
        return self.__volume_dial

    @property
    def load_profile_button(self):
        return self.__btn_load_profile

    @property
    def save_profile_button(self):
        return self.__btn_save_profile

    @property
    def un_mute_all(self):
        return self.__btn_unmute_all

    @property
    def un_solo_all(self):
        return self.__btn_unsolo_all
