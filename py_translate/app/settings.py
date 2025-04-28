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
MODELS_CACHE_DIR = os.path.join(current_module_directory, 'models_cache')

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

MAX_TEXT_LENGTH = 1000

# Models configuration --------------------------------------------------------------------
"""
NLLB-200, 196 languages, license (Creative Commons Attribution-NonCommercial 4.0)
    https://huggingface.co/facebook/nllb-200-distilled-600M
    https://huggingface.co/facebook/nllb-200-distilled-1.3B

M2M100, 100 languages, MIT
    https://huggingface.co/facebook/m2m100_418M
    https://huggingface.co/facebook/m2m100_1.2B
"""

M2M100_418 = "facebook/m2m100_418M"
M2M100_1200 = "facebook/m2m100_1.2B"
TRANSLATE_MODELS = set()
TRANSLATE_MODELS.update([M2M100_418, M2M100_1200])

SELECTED_MODEL = M2M100_418

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