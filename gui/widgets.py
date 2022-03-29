from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt, QRect


class HomeButton(QPushButton):
    def __init__(self, icone: QIcon, texte: str, parent=None):
        super(HomeButton, self).__init__()

        self.pixmap = icone.pixmap(QSize(100,100))
        self.icon = QLabel()
        self.icon.setPixmap(self.pixmap)
        
        self.setFixedSize(180, 180)
        
        self.text_label = QLabel(texte)
        self.text_label.setContentsMargins(0, 0, 0, 0)

        self.setContentsMargins(10,10,10,10)

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.icon, alignment=Qt.AlignCenter)
        lay.addWidget(self.text_label, alignment=Qt.AlignCenter)
        
        
class TextButton(QPushButton):
    def __init__(self, texte: str, parent=None):
        super(TextButton, self).__init__(parent)

        self.setText(texte)