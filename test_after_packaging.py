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

    subprocess.run(["pip", "install", "virtualenv"])
    subprocess.run(["virtualenv", r"project_sample\venv"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", r"."])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", r"aiohttp>=3.7.4.post0"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", r"pytest>=6.2.5"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", r"pytest-aiohttp>=0.3.0"])
    subprocess.run(["pytest", "tests"])

    _delete_folder(folder=r"project_sample\venv")
# ==================================================


# ==================================================
if __name__ == '__main__':
    test()
# ==================================================
