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

    subprocess.run(["pip", "install", "virtualenv"])
    subprocess.run(["virtualenv", r"project_sample\venv"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", "-r", r"project_sample\requirements\test_before_packaging.txt"])
    subprocess.run(["pytest", "tests"])

    _delete_folder(folder=r"project_sample\venv")
# ==================================================


# ==================================================
if __name__ == '__main__':
    test()
# ==================================================
