import os
from flask import Flask, request, Blueprint, make_response, send_from_directory
from app.settings import LOGS_DIR, APP_NAME
from app.routes.common.responses import ResponseMessages

import logging

logger = logging.getLogger(__name__) # getting root logger
if not logging.getLogger().hasHandlers():
    print("ERROR: Root logger had no handlers. Logging unavailable.")

logs_blueprint = Blueprint('logs_blueprint', __name__)

# ------------------------------------------------------/logs-----------------------------------------------------------
@logs_blueprint.route('/logs', methods=['GET'])
def get_logs():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        # return abort(400, description="Missing required query parameters: year, month, day.")
        return ResponseMessages.error_400("Missing required query parameters: year, month, day.")

    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except ValueError:
        # return abort(400, description="Invalid query parameters: year, month, day must be integers.")
        return ResponseMessages.error_400("Invalid query parameters: year, month, day must be integers.")

    log_filename = f"{APP_NAME}_{year:04d}-{month:02d}-{day:02d}.log"
    log_filepath = os.path.join(LOGS_DIR, log_filename)
    logger.info(f"log_filepath = {log_filepath}")

    if not os.path.isfile(log_filepath):
        return ResponseMessages.error_400(f"Log file {log_filename} not found.")

    try:
        with open(log_filepath, 'r') as file:
            log_content = file.read()
        response = make_response(log_content, 200)
        response.mimetype = "text/plain"
        return response
    except Exception as e:
        return ResponseMessages.error_500(f"Error reading file: {str(e)}")