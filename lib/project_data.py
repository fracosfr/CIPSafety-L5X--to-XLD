from audioop import add


class ProjectData():
    def __init__(self, file: str = "") -> None:
        self.file = file
        self.project_name = "New project"
        self.modules: list[ProjectDataModule] = []
        self.prefix_sdi = "Safety_inputs"
        self.prefix_sdo = "Safety_outputs"
        self.prefix_di = "Inputs"
        self.prefix_do = "Outputs"
    
    def save(self) -> bool:
        pass
    
    def load(self) -> bool:
        pass
    

class ProjectDataAddress():
    def __init__(self, type: str, addr: str, name: str, module_name : str = "") -> None:
        self.type = type
        self.name = name
        self.addr = addr
        if self.name not in ("cos", "cis", "reserved"):
            self.label = module_name + "_" + name
            self.label = self.label.replace(" ", "_")
        else:
            self.label = name
        
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
        

class ProjectDataModule():
    def __init__(self, name: str, addresses: list[ProjectDataAddress] = []) -> None:
        self.addresses = addresses
        self.name = name