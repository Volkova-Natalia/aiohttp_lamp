import os
from pathlib import Path
from dotenv import load_dotenv
from distutils.util import strtobool


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DEBUG = bool(strtobool(os.getenv('DEBUG', 'True')))

SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', '9999'))
SERVER = SERVER_HOST + ':' + str(SERVER_PORT)
