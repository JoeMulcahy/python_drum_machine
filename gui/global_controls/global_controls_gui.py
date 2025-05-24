from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QDial, QPushButton, QBoxLayout, QVBoxLayout, QGroupBox, \
    QSizePolicy

import settings


class MasterControls(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QGridLayout()

        # Unsolo, Unmute, Reset application global controls
        globals_controls_groupbox = QGroupBox("Global Controls")
        global_controls_layout = QGridLayout()

        self.__lbl_reset_mute_solo = QLabel("Reset")
        self.__btn_unmute_all = QPushButton("M")
        self.__btn_unsolo_all = QPushButton("S")
        self.__btn_reset_all = QPushButton('All')

        global_controls_layout.addWidget(self.__lbl_reset_mute_solo, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        global_controls_layout.addWidget(self.__btn_unsolo_all, 0, 1, 1, 1)
        global_controls_layout.addWidget(self.__btn_unmute_all, 0, 2, 1, 1)
        global_controls_layout.addWidget(self.__btn_reset_all, 0, 3, 1, 1)
        globals_controls_groupbox.setLayout(global_controls_layout)

        # Master Volume
        master_volume_groupbox = QGroupBox("Master Volume")
        master_volume_layout = QGridLayout()

        self.__volume_dial = QDial()
        self.__volume_dial.setFixedSize(70, 70)
        self.__volume_dial.setRange(0, 100)
        self.__volume_dial.setValue(50)
        self.__volume_dial.setWrapping(False)
        self.__volume_dial.setNotchesVisible(True)

        master_volume_layout.addWidget(self.__volume_dial, 0, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)
        master_volume_groupbox.setLayout(master_volume_layout)

        # Profile
        profile_groupbox = QGroupBox("Profile")
        profile_layout = QGridLayout()
        self.__lbl__profile = QLabel("Profile")
        self.__btn_load_profile = QPushButton("Load")
        self.__btn_save_profile = QPushButton("Save")
        profile_layout.addWidget(self.__lbl__profile, 0, 0, 1, 1)
        profile_layout.addWidget(self.__btn_load_profile, 0, 1, 1, 1)
        profile_layout.addWidget(self.__btn_save_profile, 0, 2, 1, 1)
        profile_groupbox.setLayout(profile_layout)

        main_layout.addWidget(globals_controls_groupbox, 0, 0, 1, 1)
        main_layout.addWidget(master_volume_groupbox, 1, 0, 1, 1)
        main_layout.addWidget(profile_groupbox, 2, 0, 1, 1)

        self.set_style()

        self.setLayout(main_layout)

    def set_style(self):
        for btn in [self.__btn_load_profile, self.__btn_save_profile, self.__btn_unsolo_all, self.__btn_unmute_all,
                    self.__btn_reset_all]:
            btn.setFixedSize(30, 30)
            btn.setSizePolicy(settings.FIXED_SIZE_POLICY)
            btn.setStyleSheet(settings.BUTTON_STYLE_2)

        self.__btn_reset_all.setStyleSheet(settings.RESET_BUTTON_STYLE)

        for lbl in [self.__lbl__profile, self.__lbl_reset_mute_solo]:
            lbl.setStyleSheet(settings.LABEL_STYLE_1)
            lbl.setSizePolicy(settings.FIXED_SIZE_POLICY)

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

    @property
    def reset_all_button(self):
        return self.__btn_reset_all
