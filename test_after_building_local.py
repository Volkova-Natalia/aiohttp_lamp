import os
import shutil
import subprocess


# --------------------------------------------------
def _delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
# --------------------------------------------------


# ==================================================
def test():
    _delete_folder(folder=r"project_sample\venv")
    _delete_folder(folder=r"aiohttp_lamp.egg-info")
    _delete_folder(folder=r"dist")


    subprocess.run(["python", "setup.py", "sdist"])
    subprocess.run(["pip", "install", "virtualenv"])
    subprocess.run(["virtualenv", r"project_sample\venv"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", "-r", r"project_sample\requirements\work_after_building_base.txt"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", r"dist\aiohttp_lamp-0.1.tar.gz"])
    subprocess.run(["pytest", "tests"])

    _delete_folder(folder=r"project_sample\venv")
# ==================================================


# ==================================================
if __name__ == '__main__':
    test()
# ==================================================
