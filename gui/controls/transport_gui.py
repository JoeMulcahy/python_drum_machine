from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QSpinBox, QLabel, QCheckBox, \
    QDial, QComboBox

import settings


class TransportGui(QWidget):
    def __init__(self):
        super().__init__()
        self.__is_playing = False

        # play/stop buttons
        self.__btn_play = QPushButton("Play")
        self.__btn_stop = QPushButton("Stop")

        transport_group_box = QGroupBox(f"Transport")
        transport_group_box.setStyleSheet(settings.GROUPBOX_STYLE_1)
        transport_group_box.setSizePolicy(settings.FIXED_SIZE_POLICY)
        transport_module_layout = QGridLayout()

        transport_module_layout.setSpacing(20)
        transport_module_layout.addWidget(self.__btn_play, 0, 0)
        transport_module_layout.addWidget(self.__btn_stop, 0, 1)

        self.set_style()

        transport_group_box.setLayout(transport_module_layout)
        module_layout = QGridLayout()

        module_layout.addWidget(transport_group_box)
        module_layout.setSpacing(5)
        module_layout.setContentsMargins(5, 10, 5, 5)

        self.setLayout(module_layout)

    def set_style(self):
        for btn in [self.__btn_play, self.__btn_stop]:
            btn.setFixedSize(100, 50)
            btn.setSizePolicy(settings.FIXED_SIZE_POLICY)
            btn.setStyleSheet(settings.BUTTON_STYLE_2)

    def set_is_playing(self, value):
        self.__is_playing = value

    @property
    def is_playing(self):
        return self.__is_playing

    @property
    def btn_play(self):
        return self.__btn_play

    @property
    def btn_stop(self):
        return self.__btn_stop




