from flask import request, make_response
from app.routes.common.responses import ResponseMessages
#from app.settings import AUTHORIZE

import logging
logger = logging.getLogger(__name__) # getting root logger
if not logging.getLogger().hasHandlers():
    print("ERROR: Root logger had no handlers. Logging unavailable.")

# Define a list of public endpoints
public_endpoints = ['/']

def check_authorization():
    # Check if the endpoint requires authorization
    try:

        if request.path not in public_endpoints:
            logger.info(f'----> "{request.path}" ')
            auth_header = request.headers.get('Authorization')

            status_code, error_txt = 200, ''

            if status_code == 401:
                # Return unauthorized response
                return ResponseMessages.error_401(str(error_txt)) # Stop further processing

            logger.debug('Authorization passed')

        else:
            logger.info(f'----> "{request.path}" is not protected')

    except Exception as e:
        return ResponseMessages.error_500(f"Middleware error on path {request.path}: {str(e)}")
