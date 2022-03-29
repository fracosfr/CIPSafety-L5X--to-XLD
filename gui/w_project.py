from audioop import add
from PySide6 import QtWidgets as Qw
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon

from lib.project_data import ProjectData, ProjectDataModule, ProjectDataAddress


class WProject(Qw.QWidget):
    signal_close_project = Signal()
    signal_open_project = Signal()

    def __init__(self, parent, data: ProjectData) -> None:
        super().__init__(parent)

        self._data = data

        self.main_layout = Qw.QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.row_head = Qw.QHBoxLayout()
        self.lbl_project_name = Qw.QLabel(self._data.project_name)
        self.lbl_project_name.setObjectName("title")
        self.row_head.addWidget(self.lbl_project_name)
        self.btn_edit_project_name = Qw.QPushButton(icon=QIcon("assets/edit.svg"))
        self.btn_edit_project_name.setIconSize(QSize(20, 20))
        self.btn_save = Qw.QPushButton(icon=QIcon("assets/save.svg"))
        self.btn_save.setIconSize(QSize(30, 30))
        self.btn_export = Qw.QPushButton(icon=QIcon("assets/export.svg"))
        self.btn_export.setIconSize(QSize(30, 30))
        self.btn_new = Qw.QPushButton(icon=QIcon("assets/new.svg"))
        self.btn_new.setIconSize(QSize(30, 30))
        self.btn_close = Qw.QPushButton(icon=QIcon("assets/close.svg"))
        self.btn_close.setIconSize(QSize(30, 30))
        self.btn_open = Qw.QPushButton(icon=QIcon("assets/open.svg"))
        self.btn_open.setIconSize(QSize(30, 30))
        self.btn_reload = Qw.QPushButton(icon=QIcon("assets/load.svg"))
        self.btn_reload.setIconSize(QSize(30, 30))
        self.row_head.addWidget(self.btn_edit_project_name)
        self.row_head.addStretch()
        self.row_head.addWidget(self.btn_new)
        self.row_head.addWidget(self.btn_open)
        self.row_head.addWidget(self.btn_reload)
        self.row_head.addWidget(self.btn_save)
        self.row_head.addWidget(self.btn_export)
        self.row_head.addWidget(self.btn_close)

        self.group_settings = Qw.QGroupBox("PREFIXES DES ADRESSES")
        self.grid_settings = Qw.QGridLayout()
        self.grid_settings.addWidget(Qw.QLabel("Entrées SAFETY :"), 0, 0)
        self.grid_settings.addWidget(Qw.QLabel("Sorties SAFETY :"), 1, 0)
        self.grid_settings.addWidget(Qw.QLabel("Entrées PROCESS :"), 0, 2)
        self.grid_settings.addWidget(Qw.QLabel("Sorties PROCESS :"), 1, 2)
        self.txt_prefix_sdi = Qw.QLineEdit(self._data.prefix_sdi)
        self.txt_prefix_sdo = Qw.QLineEdit(self._data.prefix_sdo)
        self.txt_prefix_di = Qw.QLineEdit(self._data.prefix_di)
        self.txt_prefix_do = Qw.QLineEdit(self._data.prefix_do)
        self.grid_settings.addWidget(self.txt_prefix_sdi, 0, 1)
        self.grid_settings.addWidget(self.txt_prefix_sdo, 1, 1)
        self.grid_settings.addWidget(self.txt_prefix_di, 0, 3)
        self.grid_settings.addWidget(self.txt_prefix_do, 1, 3)
        self.group_settings.setLayout(self.grid_settings)

        self.row_content = Qw.QHBoxLayout()
        self.row_content.setAlignment(Qt.AlignLeft)
        self.list_modules = Qw.QListWidget()
        self.list_modules.setMaximumWidth(350)
        self.list_modules.currentRowChanged.connect(self._list_addresses)
        
        self.table_data = Qw.QTableWidget()
        self.table_data.cellChanged.connect(self._save_cell_value)
        
        self.row_content.addWidget(self.list_modules)
        self.row_content.addWidget(self.table_data)

        self.main_layout.addLayout(self.row_head)
        self.main_layout.addWidget(self.group_settings)
        self.main_layout.addLayout(self.row_content)

        self._load_data()
        
        # Buttons actions
        self.btn_edit_project_name.clicked.connect(self._change_project_name)
        
        # Dynamic save inpus values
        self.txt_prefix_sdi.textChanged.connect(self._save_sdi_prefix)
        self.txt_prefix_sdo.textChanged.connect(self._save_sdo_prefix)
        self.txt_prefix_di.textChanged.connect(self._save_di_prefix)
        self.txt_prefix_do.textChanged.connect(self._save_do_prefix)
        

    def _load_data(self):
        self.lbl_project_name.setText(self._data.project_name)
        self.txt_prefix_sdi.setText(self._data.prefix_sdi)
        self.txt_prefix_sdo.setText(self._data.prefix_sdo)
        self.txt_prefix_di.setText(self._data.prefix_di)
        self.txt_prefix_do.setText(self._data.prefix_do)
        self._load_modules_list()

    def _load_modules_list(self):
        self.list_modules.clear()
        for module in self._data.modules:
            i = Qw.QListWidgetItem(module.name)
            i.module = module
            self.list_modules.addItem(i)
            
        self._list_addresses(-1)

    def _change_project_name(self):
        dialog = Qw.QInputDialog(self)
        dialog.setTextValue(self._data.project_name)
        dialog.setLabelText("Nom du projet :")
        if dialog.exec():
            self._data.project_name = dialog.textValue()
            self._load_data()
            
    def _save_sdi_prefix(self, value: str):
        self._data.prefix_sdi = value
        
    def _save_sdo_prefix(self, value: str):
        self._data.prefix_sdo = value
        
    def _save_di_prefix(self, value: str):
        self._data.prefix_di = value
        
    def _save_do_prefix(self, value: str):
        self._data.prefix_do = value
        
    def _list_addresses(self, value: int):
        self.table_data.clear()
        self.table_data.setColumnCount(0)
        self.table_data.setRowCount(0)
        if value >= 0:
            self.table_data.setColumnCount(4)
            self.table_data.setHorizontalHeaderItem(0, Qw.QTableWidgetItem("Adresse"))
            self.table_data.setHorizontalHeaderItem(1, Qw.QTableWidgetItem("Type"))
            self.table_data.setHorizontalHeaderItem(2, Qw.QTableWidgetItem("Nom"))
            self.table_data.setHorizontalHeaderItem(3, Qw.QTableWidgetItem("Mnémonique"))
            
            
            self.table_data.setRowCount(len(self._data.modules[value].addresses))
            
            index = 0
            for addr in self._data.modules[value].addresses:
                cell_address = Qw.QTableWidgetItem(addr.addr)
                cell_type = Qw.QTableWidgetItem(addr.type)
                cell_name = Qw.QTableWidgetItem(addr.name)
                cell_value = Qw.QTableWidgetItem(addr.label)
                self.table_data.setColumnWidth(3, 300)
                
                
                cell_address.setFlags(Qt.ItemIsSelectable)
                cell_type.setFlags(Qt.ItemIsSelectable)
                cell_name.setFlags(Qt.ItemIsSelectable)
                
                if addr.name in ("cos", "cis", "reserved"):
                    cell_value.setFlags(Qt.ItemIsSelectable)
                
                self.table_data.setItem(index, 0, cell_address)
                self.table_data.setItem(index, 1, cell_type)
                self.table_data.setItem(index, 2, cell_name)
                self.table_data.setItem(index, 3, cell_value)
                
                index += 1
        
        
    def _save_cell_value(self, row: int, col: int):
        cell = self.table_data.cellWidget(row, col)
        if cell:
            index_module = self.list_modules.currentRow()
            name = self.table_data.item(row, 2).text()
            type = self.table_data.item(row, 1).text()
            
            self._data.modules[index_module].addresses[row].label = cell.text()
            
            if name[0] in ("I", "O"):
                index = 0
                for addr in self._data.modules[index_module].addresses:
                    if addr.name == f"V {name[-2:]}":
                        self._data.modules[index_module].addresses[index].label = f"{cell.text()}_VALID"
                    index += 1
                self._list_addresses(index_module)
            