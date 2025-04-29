from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QDial, QPushButton, QBoxLayout, QVBoxLayout


class MasterControls(QWidget):
    def __init__(self):
        super().__init__()

        box_layout = QBoxLayout("Global Controls")
        controls_layout = QGridLayout()

        self.__lbl__volume = QLabel("Master Volume")
        self.__lbl__profile = QLabel("Profile")

        self.__volume_dial = QDial()
        self.__btn_load_profile = QPushButton("Load")
        self.__btn_save_profile = QPushButton("Save")

        controls_layout.addWidget(self.__lbl__volume, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__volume_dial, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.__lbl__profile, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
        controls_layout.addWidget(self.__btn_load_profile, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.__btn_save_profile, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        button_style = "QPushButton { font-size: 10px; }"
        for btn in [self.__btn_load_profile, self.__btn_save_profile]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(button_style)

        label_style = "QLabel { font-size: 12px; font-weight: bold; }"
        for lbl in [self.__lbl__volume, self.__lbl__profile]:
            lbl.setStyleSheet(label_style)

        box_layout.addLayout(controls_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(box_layout)
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
