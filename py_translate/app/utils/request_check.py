import json

import logging

logger = logging.getLogger(__name__) # getting root logger
if not logging.getLogger().hasHandlers():
    print("ERROR: Root logger had no handlers. Logging unavailable.")

def request_body_none_check( json_dict:dict, key_name:str):
    # value = json_dict[key_name]       - triggers error if there is no key_name
    value = json_dict.get(key_name)

    logger.info(f"{key_name}: {value}")
    error_string = ''

    if value is None:
        error_string =  f'Error: {key_name} is not defined in the body (JSON) of request.'
        logger.error(error_string)
        return None, error_string
    else:
        return value, error_string

def request_none_check( request, name:str, is_header: bool = False ):
    value = request.headers.get(name) if is_header else request.args.get(name)

    logger.info(f"{name}: {value}")
    error_string = ''

    if value is None:
        error_string =  f'Error: {name} {"header" if is_header else "parameter"} is not defined'
        logger.error(error_string)
        return None, error_string
    else:
        return value, error_string

def request_str_guids_check( request, header_name:str ):
    str_guids = None
    error_string = ''
    str_guids_header = request.headers.get(header_name)

    if str_guids_header:
        try:
            # Parsing as JSON
            str_guids = json.loads(str_guids_header)

            # Checking if the result is a list of strings
            if isinstance(str_guids, list) and all(isinstance(guid, str) for guid in str_guids):
                logger.info(f"{header_name}: {str_guids}")
            else:
                error_string = f'Error: {header_name} must be a list of strings'

            if not str_guids:
                str_guids = None

        except json.JSONDecodeError as e:
            error_string=f'Error: Unable to parse {header_name} as JSON - {e}'
            logger.error(error_string)

    if str_guids is None:
        if not error_string:
            error_string = f'Error: {header_name} header is missing or empty'
        logger.error(error_string)
        return None, error_string
    else:
        return str_guids, error_string

def request_attributes_check( attributes_header ):
    error_string = ''
    attributes_data = None

    if attributes_header:
        try:
            # JSON into dictionary
            data = json.loads(attributes_header)

            # Checking that data is a list of objects
            if not isinstance(data, list) or not all(isinstance(obj, dict) for obj in data):
                error_string='JSON in the "attributes" header should be an array of objects'
                logger.error(f"{error_string}. Received: {attributes_header}")
                attributes_data = None
            else:
                # Convert the keys of each object in the array to lowercase
                attributes_data = [
                    {key.lower(): value for key, value in obj.items()}
                    for obj in data
                ]

                if not attributes_data:
                    attributes_data = None

        except json.JSONDecodeError as e:
            error_string = f'Error: Unable to parse "attributes" header as JSON - {e}'
            logger.error(f"{error_string}. Raw data: {attributes_header}")
            attributes_data = None

    if attributes_data is None:
        logger.error(error_string)
        return None, error_string
    else:
        return attributes_data, error_string

def request_log( request, endpoint_name:str):
    logger.info(f"------------------ {endpoint_name} ---------------- ")

    logger.info("Headers:")
    for header, value in request.headers.items():
        logger.info(f"{header}: {value}")

    logger.info("Query Parameters:")
    for key, value in request.args.items():
        logger.info(f"{key}: {value}")

    logger.info("------------------ raw body ---------------- ")

    raw_body = request.get_data()
    logger.info(raw_body)

    logger.info("------------------ end body ---------------- ")