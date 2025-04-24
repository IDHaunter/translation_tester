import html
import json
from flask import make_response, Response, jsonify
import logging
from typing import Dict, Any #, Optional

logger = logging.getLogger(__name__)


class ResponseMessages:
    # Basic messages
    ERROR_400 = {"code": 400, "title": "Bad request"}
    ERROR_401 = {"code": 401, "title": "Unauthorized"}
    ERROR_403 = {"code": 403, "title": "Forbidden"}
    ERROR_404 = {"code": 404, "title": "Not found"}
    ERROR_500 = {"code": 500, "title": "Internal server error"}

    _debug = True
    _default_format = 'json'  # may be 'text' or 'json'

    @classmethod
    def set_debug(cls, value: bool):
        cls._debug = value # Changes through cls (class) affect the entire class, not a single instance (self)

    @classmethod
    def set_default_format(cls, format_type: str):
        """Set default response format ('text' or 'json')"""
        if format_type.lower() in ('text', 'json'):
            cls._default_format = format_type.lower()
        else:
            raise ValueError("Format must be either 'text' or 'json'")

    @staticmethod
    def _build_error_payload(
            error_data: Dict[str, Any],
            details: str = '',
            debug_details: str = ''
    ) -> Dict[str, Any]:
        payload = {
            "status": "error",
            "error": {
                "code": error_data["code"],
                "title": error_data["title"],
                "message": html.escape(details) if details else error_data["title"] # protect from harmful input
            }
        }

        if ResponseMessages._debug and debug_details:
            payload["error"]["debug"] = html.escape(debug_details) # protect from harmful input

        return payload

    @staticmethod
    def _create_error_response(
            error_data: Dict[str, Any],
            details: str = '',
            debug_details: str = '',
            response_format: str = None
    ) -> Response:
        fmt = response_format or ResponseMessages._default_format

        # Logging
        log_msg = f"Error {error_data['code']}: {error_data['title']} - {details}"
        if error_data["code"] == 404:
            logger.warning(log_msg)
        else:
            logger.error(log_msg)

        if fmt == 'json':
            # JSON format
            payload = ResponseMessages._build_error_payload(
                error_data, details, debug_details)

            response = make_response(json.dumps(payload), error_data["code"])
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            # Text format
            message = f"{error_data['title']}: {html.escape(details)}".strip() # protect from harmful input
            if ResponseMessages._debug and debug_details:
                message += f" (Debug: {html.escape(debug_details)})" # protect from harmful input
            return make_response(message, error_data["code"])

    @staticmethod
    def error_400(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages.ERROR_400, details, debug_details, response_format)

    @staticmethod
    def error_401(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages.ERROR_401, details, debug_details, response_format)

    @staticmethod
    def error_403(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages.ERROR_403, details, debug_details, response_format)

    @staticmethod
    def error_404(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages.ERROR_404, details, debug_details, response_format)

    @staticmethod
    def error_500(details: str = '', debug_details: str = '', response_format: str = None) -> Response:
        return ResponseMessages._create_error_response(
            ResponseMessages.ERROR_500, details, debug_details, response_format)

    # Success methods
    @staticmethod
    def success(message: str = '', data: dict = None, status_code: int = 200) -> Response:
        payload = {
            "status": "success",
            "code": status_code,
            "message": message
        }
        if data is not None:
            payload["data"] = data
        return jsonify(payload), status_code
