from PySide6.QtWidgets import QWidget, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from fun import asset_file

from gui.widgets import HomeButton


class WEmpty(QWidget):
    signal_open_project = Signal(str)
    signal_new_project = Signal(str)

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.btn_new_project = HomeButton(QIcon(asset_file("new.svg")), "Nouveau projet")
        self.btn_open_project = HomeButton(QIcon(asset_file("open.svg")), "Ouvrir un projet")

        self.row = QHBoxLayout(self)
        self.row.setAlignment(Qt.AlignCenter)
        self.row.addWidget(self.btn_new_project)
        self.row.addSpacing(20)
        self.row.addWidget(self.btn_open_project)

        self.btn_new_project.clicked.connect(self._new_project_button_action)
        self.btn_open_project.clicked.connect(self._open_project_button_action)

    def _new_project_button_action(self):
        file_path, result = QFileDialog.getOpenFileName(
            self, "Fichier L5X", "", "Fichier .l5x (*.l5x)")
        if result:
            self.signal_new_project.emit(file_path)

    def _open_project_button_action(self):
        file_path, result = QFileDialog.getOpenFileName(
            self, "Charger un projet existant", "", "Projet L5X TO XLD (*.l5x2xld)")
        if result:
            self.signal_open_project.emit(file_path)
