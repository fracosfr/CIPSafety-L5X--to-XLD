from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui import style
from fun import asset_file

app = QApplication()
w = MainWindow()
w.show()

with open(asset_file("style.css"), "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

app.exec()