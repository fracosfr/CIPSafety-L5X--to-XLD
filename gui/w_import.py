from PySide6.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal, Qt

import os
from gui.widgets import TextButton
from lib.l5x_file import L5xFile

from lib.project_data import ProjectData, ProjectDataAddress, ProjectDataModule


class WImport(QWidget):
    signal_cancel = Signal()
    signal_start_project = Signal(ProjectData)
    
    def __init__(self, parent, l5x_file: str = "") -> None:
        super().__init__(parent)
        self._data = ProjectData()
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)
        
        if l5x_file:
            if not os.path.exists(l5x_file) or not os.path.isfile(l5x_file):
                QMessageBox.critical(self, "ERREUR !", "Le fichier fourni est corrompu ou inexistant !")
                self.signal_cancel.emit()
                
            self.lbl_project_name = QLabel("Nom du projet :")
            self.lbl_project_name.setObjectName("title")
            
            self.txt_nom_projet = QLineEdit(self._data.project_name)
            self.txt_nom_projet.setObjectName("title")
            
            self.row_title = QHBoxLayout()
            self.row_title.addWidget(self.lbl_project_name)
            self.row_title.addSpacing(20)
            self.row_title.addWidget(self.txt_nom_projet)
            self.main_layout.addLayout(self.row_title)

            self.row_content = QHBoxLayout()
            self.list_modules = QListWidget()
            self.list_addr = QListWidget()
            self.row_content.addWidget(self.list_modules)
            self.row_content.addWidget(self.list_addr)
            self.main_layout.addLayout(self.row_content)
            self.list_modules.currentRowChanged.connect(self._fill_addresses)
            
            # BUTTONS
            self.row_bottons = QHBoxLayout()
            self.btn_cancel = TextButton("ANNULER")
            self.btn_cancel.setObjectName("red")
            self.btn_next = TextButton("CRÉER LE PROJET")
            self.btn_cancel.clicked.connect(self.signal_cancel)
            self.btn_next.clicked.connect(self._start_project)
            self.row_bottons.addWidget(self.btn_cancel, alignment=Qt.AlignLeft)
            self.row_bottons.addWidget(self.btn_next, alignment=Qt.AlignRight)
            self.main_layout.addLayout(self.row_bottons)
            
            # Loading L5X FILE
            l5x = L5xFile(l5x_file)
            self._data.l5x_file = l5x
            
            modules: dict[ProjectDataModule] = {}
            
            for module in l5x.sdi:
                if module.name != "reserved":
                    addrs = []
                    for ad in module.values:
                        addrs.append(ProjectDataAddress("SAFE INPUT", module.operand, ad.operand[1:], ad.name, module.name[:9]))

                    if not modules.get(module.name):
                        modules[module.name] = ProjectDataModule(module.name, addrs)
                    else:
                        modules[module.name].addresses += addrs
                        
            for module in l5x.sdo:
                if module.name != "reserved":
                    addrs = []
                    for ad in module.values:
                        addrs.append(ProjectDataAddress("SAFE OUTPUT", module.operand, ad.operand[1:], ad.name, module.name[:9]))
                    
                    if not modules.get(module.name):
                        modules[module.name] = ProjectDataModule(module.name, addrs)
                    else:
                        modules[module.name].addresses += addrs
                        
            for module in l5x.di:
                if module.name != "reserved":
                    addrs = []
                    for ad in module.values:
                        addrs.append(ProjectDataAddress("INPUT", module.operand, ad.operand[1:], ad.name, module.name[:9]))
                    
                    if not modules.get(module.name):
                        modules[module.name] = ProjectDataModule(module.name, addrs)
                    else:
                        modules[module.name].addresses += addrs
                        
            for module in l5x.do:
                if module.name != "reserved":
                    addrs = []
                    for ad in module.values:
                        addrs.append(ProjectDataAddress("OUTPUT", module.operand, ad.operand[1:], ad.name, module.name[:9]))
                    
                    if not modules.get(module.name):
                        modules[module.name] = ProjectDataModule(module.name, addrs)
                    else:
                        modules[module.name].addresses += addrs
            
            self._data.modules.clear()    
            for module_name in sorted(modules.keys()):
                self._data.modules.append(modules[module_name])
                
            for module in self._data.modules:
                list_item = QListWidgetItem(module.name)
                self.list_modules.addItem(list_item)
                
    def _fill_addresses(self, index: int):
        self.list_addr.clear()
        for addr in self._data.modules[index].addresses:
            i = QListWidgetItem(addr.name)
            self.list_addr.addItem(i)
            
    def _start_project(self):
        self._data.project_name = self.txt_nom_projet.text()
        if not self._data.project_name:
            self._data.project_name = "New project"
        
        self._data.initialise()
        self.signal_start_project.emit(self._data)