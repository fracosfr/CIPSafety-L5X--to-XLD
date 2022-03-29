from PySide6.QtWidgets import QApplication
from PySide6 import QtCore

from gui.main_window import MainWindow
from fun import asset_file

app = QApplication()
w = MainWindow()
w.show()

with open(asset_file("style.css"), "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

locale = QtCore.QLocale.system().name()
translator = QtCore.QTranslator()
reptrad = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
translator.load("qtbase_" + locale, reptrad)
app.installTranslator(translator)

app.exec()