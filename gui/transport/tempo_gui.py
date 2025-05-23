from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel


class TempoGui(QWidget):
    def __init__(self):
        super().__init__()

        # tempo spinbox
        self.__tempo_spin_box = QSpinBox()
        self.__tempo_spin_box.setRange(1, 300)
        self.__tempo_spin_box.setValue(120)

        self.__lbl_bpm = QLabel("bpm")