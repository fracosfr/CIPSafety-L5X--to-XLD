import os

upx_dir = 'C:\\upx'
param_upx = ""


if os.path.exists(upx_dir):
    param_upx = f"--upx-dir \"{upx_dir}\""
    

datas = []

for file in os.listdir("assets"):
    datas.append(f"--add-data assets/{file};assets/")

data = " ".join(datas)
os.system(f"pyinstaller main.py -F -w -i assets/icon.ico -n L5X_TO_XLD -y {param_upx} {data}")