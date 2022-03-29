import sys, os

def asset_file(file: str):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath('.')), "assets", file)
