from os import path
from lxml import etree

from lib.l5x_io import L5xAddress, L5xModule


class L5xFile():
    def __init__(self, file_path: str) -> None:
        self.sdi:list[L5xModule] = []
        self.sdo:list[L5xModule] = []
        self.di:list[L5xModule] = []
        self.do:list[L5xModule] = []
        if path.exists(file_path) and path.isfile(file_path):
            self.file_path = file_path
            self.parse()
        else:
            self.file_path = ""

    def parse(self) -> None:
        if self.file_path:
            try:
                xml_content = etree.parse(self.file_path)
                root = xml_content.getroot()
                for type in xml_content.xpath("/RSLogix5000Content/Module/Communications/Connections/Connection"):
                    type_name = type.get("Name")
                    if type_name == "SafetyInput":
                        current_module_name = ""
                        current_operand = ""
                        current_module_values = []
                        for el in type.xpath("InputTag/Comments/Comment"):
                            operand = el.get("Operand")
                            if operand[-1] == "]":
                                if current_operand:
                                    self.sdi.append(
                                        L5xModule(current_operand, current_module_name, current_module_values))
                                current_operand = operand[6:-1]
                                current_module_name = el.text
                                current_module_values = []
                            else:
                                current_module_values.append(
                                    L5xAddress(operand[-2:], el.text))
                        self.sdi.append(L5xModule(current_operand, current_module_name, current_module_values))
                    elif type_name == "SafetyOutput":
                        current_module_name = ""
                        current_operand = ""
                        current_module_values = []
                        for el in type.xpath("OutputTag/Comments/Comment"):
                            operand = el.get("Operand")
                            if operand[-1] == "]":
                                if current_operand:
                                    self.sdo.append(
                                        L5xModule(current_operand, current_module_name, current_module_values))
                                current_operand = operand[6:-1]
                                current_module_name = el.text
                                current_module_values = []
                            else:
                                current_module_values.append(
                                    L5xAddress(operand[-2:], el.text))
                        self.sdo.append(L5xModule(current_operand, current_module_name, current_module_values))
                    elif type_name == "Standard":
                        current_module_name = ""
                        current_operand = ""
                        current_module_values = []
                        for el in type.xpath("InputTag/Comments/Comment"):
                            operand = el.get("Operand")
                            if operand[-1] == "]":
                                if current_operand:
                                    self.di.append(
                                        L5xModule(current_operand, current_module_name, current_module_values))
                                current_operand = operand[6:-1]
                                current_module_name = el.text
                                current_module_values = []
                            else:
                                current_module_values.append(
                                    L5xAddress(operand[-2:], el.text))
                        self.di.append(L5xModule(current_operand, current_module_name, current_module_values))
                        current_module_name = ""
                        current_operand = ""
                        current_module_values = []
                        for el in type.xpath("OutputTag/Comments/Comment"):
                            operand = el.get("Operand")
                            if operand[-1] == "]":
                                if current_operand:
                                    self.do.append(
                                        L5xModule(current_operand, current_module_name, current_module_values))
                                current_operand = operand[6:-1]
                                current_module_name = el.text
                                current_module_values = []
                            else:
                                current_module_values.append(
                                    L5xAddress(operand[-2:], el.text))
                        self.do.append(L5xModule(current_operand, current_module_name, current_module_values))
            except:
                pass

    def export(self, file_dest: str):
        pass