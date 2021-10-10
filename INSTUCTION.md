# How to write an Packaging Python Project
You have to use the following architecture in your project:  
<details>  
<summary>show the architecture</summary>  

```
aiohttp_lamp/
|
|__ aiohttp_lamp/
|   |__ __init__.py
|   |__ ...
|
|__ tests/
    |__ __init__.py
    |__ ...
```
</details>  


<br>  



___
## Testing your Project  
You should create sample project:  
<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
    |__ src/
    |   |__ __init__.py
    |   |__ ...
    |
    |__ requirements/
    |   |__ ...
    |
    |__ .env
    |__ .env.sample
    |__ requirements.txt
```
</details>  

<br>


### Testing your Packaging Project  
You should add test script **test_before_packaging.py**.  
<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
|   |__ ...
|
|__ test_before_packaging.py
```
</details>  

<details>  
<summary>show 'test_before_packaging.py' code</summary>  

```python
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
```
</details>  

<br>

To test your project you can use script **test_before_packaging.py**:
```
path_to_aiohttp_lamp: test_before_packaging.py
```  


<br>





___
## Packaging your Project

### Add files README.md and LICENSE  
<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
|   |__ ...
|
|__ test_before_packaging.py
|
|__ README.md
|__ LICENSE
```
</details>  

<br>

### Defining your Installable Package with setup.cfg 
This **setup.cfg** file describes the package that you’ll build.  
<details>
<summary>show 'setup.cfg' code</summary>  

```python
[metadata]
name = aiohttp_lamp
version = 0.1
description = Packaged WebSocket client to manage a lamp (using aiohttp).
long_description = file: README.md
url = https://github.com/Volkova-Natalia/aiohttp_lamp
author = Volkova Natalia
license = MIT
classifiers =
    Environment :: Web Environment
    Intended Audience :: Developers
    License :: OSI Approved :: MIT License
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.8
    Topic :: Software Development :: Libraries :: Python Modules

[options]
include_package_data = True
packages = find:
python_requires = >=3.8
install_requires =
    aiohttp>=3.7.4.post0
    pytest>=6.2.5
    pytest-aiohttp>=0.3.0
```
</details>    

<br>

Else, you need a **setup.py** script, which will automatically use your **setup.cfg** file.  
<details>
<summary>show 'setup.py' code</summary>  

```python
if __name__ == "__main__":
    from setuptools import setup

    setup()
```
</details>  

<br>

Only Python modules and packages will be included in the package by default.
You need a **MANIFEST.in** file to include additional files.  
<details>
<summary>show 'MANIFEST.in' code</summary>  

```text
include LICENSE
include README.md
```
</details> 

<br>

It’s considered best practice to include a **pyproject.toml** file with your package.  
<a href=https://snarky.ca/what-the-heck-is-pyproject-toml>An article on the subject</a> can run you through the details.  
<details>
<summary>show 'pyproject.toml' code</summary>  

```text
[build-system]
requires = ["setuptools >= 53.0.0", "wheel >= 0.36.2"]
build-backend = "setuptools.build_meta"
```
</details> 

<br>


<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
|   |__ ...
|
|__ test_before_packaging.py
|
|__ README.md
|__ LICENSE
|
|__ setup.cfg
|__ setup.py
|__ MANIFEST.in
|__ pyproject.toml
```
</details>  

<br>

### Testing your Installable Package  
You should add test script **test_after_packaging.py**.  
<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
|   |__ ...
|
|__ test_before_packaging.py
|__ test_after_packaging.py
|
|__ README.md
|__ LICENSE
|
|__ setup.cfg
|__ setup.py
|__ MANIFEST.in
|__ pyproject.toml
```
</details>  

<details>  
<summary>show 'test_after_packaging.py' code</summary>  

```python
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
    # subprocess.run([r"project_sample\venv\Scripts\pip", "install", "-r", r"project_sample\requirements\test_after_packaging.txt"])
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
```
</details>  

<br>

To test your project you can use script **test_after_packaging.py**:
```
path_to_aiohttp_lamp: test_after_packaging.py
```  


<br>






___
## Building your Package  
Using the command:  
```
(venv) path_to_aiohttp_lamp: python setup.py sdist
```  
This creates a directory called **dist** and builds your new package, **aiohttp_lamp-0.1.tar.gz**.  

<br>

<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ dist/
|   |__ aiohttp_lamp-0.1.tar.gz
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
|   |__ ...
|
|__ test_before_packaging.py
|__ test_after_packaging.py
|
|__ README.md
|__ LICENSE
|
|__ setup.cfg
|__ setup.py
|__ MANIFEST.in
|__ pyproject.toml
```
</details>  

<br>

### Testing your Built Package  
You should add test scripts **test_after_building_local.py** and **test_after_building_commit.py**.  
<details>  
<summary>show the directory structure</summary>  

```
aiohttp_lamp/
|
|__ dist/
|   |__ aiohttp_lamp-0.1.tar.gz
|
|__ aiohttp_lamp/
|   |__ ...
|
|__ project_sample/
|   |__ ...
|
|__ test_before_packaging.py
|__ test_after_packaging.py
|__ test_after_building_local.py
|__ test_after_building_commit.py
|
|__ README.md
|__ LICENSE
|
|__ setup.cfg
|__ setup.py
|__ MANIFEST.in
|__ pyproject.toml
```
</details>  

<details>  
<summary>show 'test_after_building_local.py' code</summary>  

```python
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
    # subprocess.run([r"project_sample\venv\Scripts\pip", "install", "-r", r"project_sample\requirements\work_after_building_local.txt"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", "-r", r"project_sample\requirements\work_after_building_base.txt"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", r"dist\aiohttp_lamp-0.1.tar.gz"])
    subprocess.run(["pytest", "tests"])

    _delete_folder(folder=r"project_sample\venv")
# ==================================================


# ==================================================
if __name__ == '__main__':
    test()
# ==================================================
```
</details>  

<details>  
<summary>show 'test_after_building_commit.py' code</summary>  

```python
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
    subprocess.run(["virtualenv", r"project_sample\\venv"])
    subprocess.run([r"project_sample\venv\Scripts\pip", "install", "-r", r"project_sample\requirements\work_after_building_commit.txt"])
    subprocess.run(["pytest", "tests"])

    _delete_folder(folder=r"project_sample\venv")
# ==================================================


# ==================================================
if __name__ == '__main__':
    test()
# ==================================================
```
</details>  

<br>

To test your project you can use script **test_after_building_local.py**:
```
path_to_aiohttp_lamp: test_after_building_local.py
```  

<br>

Or, if you committed the source archive and want to work with it, you can use script **test_after_building_commit.py**:  
```
path_to_aiohttp_lamp: test_after_building_commit.py
```  

<br>










<br>

<br>



___
## Docs, Articles & Sources
* <a href=https://snarky.ca/what-the-heck-is-pyproject-toml>What the heck is pyproject.toml?</a>  
* <a href=https://packaging.python.org/tutorials/packaging-projects/>Packaging Python Projects</a>  
* <a href=https://realpython.com/installable-django-app/>How to Write an Installable Django App</a>  
