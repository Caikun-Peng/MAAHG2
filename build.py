import PyInstaller.__main__
import os
import site

# 获取 site-packages 目录列表
site_packages_paths = site.getsitepackages()

# 查找包含 maa/bin 的路径
maa_bin_path = None
for path in site_packages_paths:
    potential_path = os.path.join(path, 'maa', 'bin')
    if os.path.exists(potential_path):
        maa_bin_path = potential_path
        break

if maa_bin_path is None:
    raise FileNotFoundError("未找到包含 maa/bin 的路径")

# 构建 --add-data 参数
add_data_param = f'{maa_bin_path}{os.pathsep}maa/bin'

# 查找包含 MaaAgentBinary 的路径
maa_bin_path2 = None
for path in site_packages_paths:
    potential_path = os.path.join(path, 'MaaAgentBinary')
    if os.path.exists(potential_path):
        maa_bin_path2 = potential_path
        break

if maa_bin_path2 is None:
    raise FileNotFoundError("未找到包含 MaaAgentBinary 的路径")

# 构建 --add-data 参数
add_data_param2 = f'{maa_bin_path2}{os.pathsep}MaaAgentBinary'


# 运行 PyInstaller
PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--name=MAAHG2',
    f'--add-data={add_data_param}',
    f'--add-data={add_data_param2}',
    '--clean',
])

import shutil

source_path = './dist/MAAHG2.exe'
destination_path = './'

try:
    shutil.move(source_path, destination_path)
    print(f"File moved successfully from {source_path} to {destination_path}")
except FileNotFoundError:
    print("The source or destination path does not exist")
except PermissionError:
    print("You do not have permission to move the file")
except Exception as e:
    print("Error occurred while moving the file:", e)

def remove_file(file_path):
    try:
        os.remove(file_path)  # 或者使用 os.unlink(file_path)
        print("File removed successfully")
    except FileNotFoundError:
        print("File does not exist")
    except PermissionError:
        print("You do not have permission to delete this file")
    except Exception as e:
        print("Error occurred:", e)

def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print("Folder and all its contents removed successfully")
    except Exception as e:
        print("Error occurred while deleting folder:", e)

remove_folder("build")
remove_folder("dist")

remove_file("MAAHG2.spec")