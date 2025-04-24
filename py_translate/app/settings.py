import configparser
import os
from dotenv import load_dotenv
from app.routes.common.responses import ResponseMessages

current_module_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.join(current_module_directory, os.pardir)

# Config constants ------------------------------------------------------------------------
SETTINGS_INI_PATH = os.path.join(os.path.dirname(current_module_directory), 'settings.ini')
LOGS_DIR = os.path.join(current_module_directory, 'logs')      # logs dir
UPLOAD_DIR = os.path.join(current_module_directory, 'tmp')     # dir for temporary files
ASSETS_DIR = os.path.join(current_module_directory, 'assets')  # dir for persistent files
DOTENV_PATH = os.path.join(ASSETS_DIR, '.env')                 # environmental variables file

APP_NAME = 'py_translate'
APP_VER = {'ver': '0.0.1',
           'date': '2025.04.24',
           'info': 'Initial version'}

import logging
from app.utils.module_logger import ModuleLogger
module_logger = ModuleLogger(module_name = APP_NAME, log_dir=LOGS_DIR, log_level=logging.DEBUG)
logger = module_logger.get_logger()

# Load env vars from .env
load_dotenv(DOTENV_PATH)

# Config variables reading from settings.ini ----------------------------------------------
config = configparser.ConfigParser()
config.read(SETTINGS_INI_PATH)

APP_MODE = config.get('Main', 'app_mode')
DEBUG = config.getboolean(APP_MODE, 'debug_mode')
HOST = config.get(APP_MODE, 'server_host')
PORT = int ( config.get(APP_MODE, 'server_port') )

tmp_str = config.get(APP_MODE, 'auth_mode').upper()
AUTHORIZE = True if tmp_str=='TRUE' else False

ResponseMessages.set_debug(DEBUG) # allow additional debug messages in responses