import os, json



class ProjectData():
    def __init__(self, file: str = "") -> None:
        self.file = file
        self.project_name = "New project"
        self.modules: list[ProjectDataModule] = []
        self.prefix_sdi = "SDI"
        self.prefix_sdo = "SDO"
        self.prefix_di = "DI"
        self.prefix_do = "DO"
    
    def initialise(self):
        self.prefix_sdi = self.project_name.replace(" ", "_") + "_SAFE"
        self.prefix_sdo = self.project_name.replace(" ", "_") + "_SAFE"
        self.prefix_di = self.project_name.replace(" ", "_")
        self.prefix_do = self.project_name.replace(" ", "_")

    def save(self) -> bool:
        data_json = {
            "project": self.project_name,
            "prefix": {
                "SDI": self.prefix_sdi,
                "SDO": self.prefix_sdo,
                "DI": self.prefix_di,
                "DO": self.prefix_do,
            },
            "modules": [o.get_data() for o in self.modules]
        }
        try:
            with open(self.file, "w") as f:
                json.dump(data_json, f, indent=4)
            return True
        except:
            return False
    
    def load(self) -> bool:
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
                if data["project"]:
                    self.project_name = data["project"]
                
                
                if data["prefix"]:
                    prefix_db = data["prefix"]
                    if prefix_db["SDI"]:
                        self.prefix_sdi = prefix_db["SDI"]
                    if prefix_db["SDO"]:
                        self.prefix_sdo = prefix_db["SDO"]
                    if prefix_db["DI"]:
                        self.prefix_di = prefix_db["DI"]
                    if prefix_db["DO"]:
                        self.prefix_do = prefix_db["DO"]
                
                if data["modules"]:
                    for module_db in data["modules"]:
                        address: list[ProjectDataAddress] = []
                        module_name = "ERROR"
                        if module_db["name"]:
                            module_name = module_db["name"]

                        if module_db["addresses"]:
                            for address_db in module_db["addresses"]:
                                add_name = address_db["name"] if address_db["name"] else "ERROR"
                                add_byte = address_db["byte"] if address_db["byte"] else "ERROR"
                                add_bit = address_db["bit"] if address_db["bit"] else "ERROR"
                                add_label = address_db["label"] if address_db["label"] else "ERROR"
                                add_type = address_db["type"] if address_db["type"] else "ERROR"
                                address.append(ProjectDataAddress(add_type, add_byte, add_bit, add_name, module_name, add_label))

                        self.modules.append(ProjectDataModule(module_name, address))

            return True
        except:
            return False
    

class ProjectDataAddress():
    def __init__(self, type: str, byte: str, bit: str, name: str, module_name : str = "", label: str = "") -> None:
        self.type = type
        self.name = name
        self.addr = f"{byte}.{bit}"
        self.byte = byte
        self.bit = bit
        if not label:
            if self.name not in ("cos", "cis", "reserved"):
                self.label = module_name + "_" + name
                self.label = self.label.replace(" ", "_")
            else:
                self.label = name
        else:
            self.label = label
        
    @property
    def get_type(self):
        if self.type == "SAFETY":
            if self.name == "cos" or self.name == "cis":
                return "SYSTEM"
            elif self.name[0] == "V":
                return "VALID"
            elif self.name[0] == "I":
                return "SAFETY INPUT"
            elif self.name[0] == "O":
                return "SAFETY OUTPUT"
            else:
                return ""
        else:
            if self.name[0] == "I":
                return "STANDARD INPUT"
            elif self.name[0] == "O":
                return "STANDARD OUTPUT"
            else:
                return ""
        
    def get_data(self):
        return {
            "name": self.name,
            "type": self.type,
            "byte": self.byte,
            "bit": self.bit,
            "label": self.label
        }

class ProjectDataModule():
    def __init__(self, name: str, addresses: list[ProjectDataAddress] = []) -> None:
        self.addresses = addresses
        self.name = name

    def get_data(self):
        return {
            "name": self.name,
            "addresses": [o.get_data() for o in self.addresses],
        }
