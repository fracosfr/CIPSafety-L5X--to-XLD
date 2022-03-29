from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

from gui.w_empty import WEmpty
from gui.w_import import WImport
from gui.w_project import WProject
from lib.project_data import ProjectData

class MainWindow (QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("CIP Safety - L5X TO XLD")
        self.setFixedSize(1100, 800)
                
        # Show main content
        self._show_empty_page()
        
        
        
        
        
    def _empty_new_project(self, file:str):
        self._show_import_page(file)
        
    def _empty_open_project(self, file:str):
        print(file)
        
    def _import_canceled_signal(self):
        self._show_empty_page()
        
    def _show_empty_page(self):
        self.empty_page = WEmpty(self)
        self.setCentralWidget(self.empty_page)
        self.empty_page.signal_new_project.connect(self._empty_new_project)
        self.empty_page.signal_open_project.connect(self._empty_open_project)
        
        
    def _show_import_page(self, file:str):
        self.import_page = WImport(self, file)
        self.import_page.signal_cancel.connect(self._import_canceled_signal)
        self.import_page.signal_start_project.connect(self._show_project_page)
        self.setCentralWidget(self.import_page)
        
    def _show_project_page(self, data: ProjectData):
        self.project_page = WProject(self, data)
        self.project_page.signal_close_project.connect(self._show_empty_page)
        self.project_page.signal_open_project.connect(self._show_empty_page)
        self.setCentralWidget(self.project_page)