from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui import style

app = QApplication()
w = MainWindow()
w.show()

#with open("assets/style.css", "r") as f:
#    _style = f.read()
app.setStyleSheet(style.CSS)

app.exec()