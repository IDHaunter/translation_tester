print('---> WSGI is starting ... ')
import sys
# print('---> sys.path wsgi :',sys.path)

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app