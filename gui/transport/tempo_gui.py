from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QGroupBox, QGridLayout

import settings


class TempoGui(QWidget):
    def __init__(self):
        super().__init__()

        # tempo spinbox
        self.__tempo_spin_box = QSpinBox()
        self.__tempo_spin_box.setRange(1, 300)
        self.__tempo_spin_box.setValue(120)

        self.__lbl_bpm = QLabel("bpm")

        tempo_group_box = QGroupBox("Tempo")
        tempo_module_layout = QGridLayout()

        tempo_module_layout.addWidget(self.__lbl_bpm, 0, 0)
        tempo_module_layout.addWidget(self.__tempo_spin_box, 0, 1)

        self.set_style()  # set widgets style

        tempo_group_box.setLayout(tempo_module_layout)
        module_layout = QGridLayout()

        module_layout.addWidget(tempo_group_box, 1, 0)

        self.setLayout(module_layout)

    def set_style(self):
        for comp in [self.__tempo_spin_box]:
            comp.setFixedSize(100, 50)

        self.__lbl_bpm.setStyleSheet(settings.TEXT_STYLE_1)

        self.__tempo_spin_box.setStyleSheet(settings.TEMPO_SPINBOX_STYLE)

    @property
    def tempo_spinbox(self):
        return self.__tempo_spin_box
