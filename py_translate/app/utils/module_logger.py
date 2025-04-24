import logging
import os
import sys
import re
from datetime import datetime

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO, is_stderr=False):
        self.logger = logger
        self.log_level = log_level
        self.is_stderr = is_stderr
        self.linebuf = ''

    def write(self, buf):
        # Remove ANSI control characters (e.g. \x1b[A\x1b[A)
        buf_cleaned = re.sub(r'\x1b\[[0-9;]*[mK]', '', buf).strip()
        buf_cleaned = "\n".join(filter(bool, buf_cleaned.splitlines()))

        if not buf_cleaned:
            return  # Skipping empty lines

        # Log stderr as ERROR only if the message looks like an error
        if self.is_stderr:
            level = logging.ERROR if re.search(r'\b(error|exception)\b', buf_cleaned, re.IGNORECASE) else self.log_level
        else:
            level = self.log_level

        for line in buf_cleaned.splitlines():
            self.logger.log(level, line.rstrip())

    def flush(self):
        pass

class DateRotatingFileHandler(logging.FileHandler):
    def __init__(self, log_dir, module_name, log_level=logging.DEBUG):
        self.log_dir = log_dir
        self.module_name = module_name
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        log_filename = f'{self.module_name}_{self.current_date}.log'
        log_filepath = os.path.join(self.log_dir, log_filename)
        super().__init__(log_filepath)
        self.setLevel(log_level)
        # This formatter is responsible for logs that are written to files.
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))

    def emit(self, record):
        new_date = datetime.now().strftime('%Y-%m-%d')
        if new_date != self.current_date:
            self.current_date = new_date
            log_filename = f'{self.module_name}_{self.current_date}.log'
            log_filepath = os.path.join(self.log_dir, log_filename)
            self.stream.close()
            self.baseFilename = log_filepath
            self.stream = self._open()
        super().emit(record)

class ModuleLogger:
    def __init__(self, module_name, log_dir='logs', log_level=logging.DEBUG):
        self.module_name = module_name
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = logging.getLogger(self.module_name)
        self._setup_logger()

    def _setup_logger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Set up the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        if not root_logger.hasHandlers():
            # File handler with date rotation
            file_handler = DateRotatingFileHandler(self.log_dir, self.module_name, self.log_level)
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)

            # Formatter (This formatter is responsible for the logs that are written to console)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
            console_handler.setFormatter(formatter)

            # Adding handlers to root logger
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)

        # Redirect stdout to INFO, stderr — filter errors
        sys.stdout = StreamToLogger(root_logger, logging.INFO, is_stderr=False)
        sys.stderr = StreamToLogger(root_logger, logging.INFO, is_stderr=True)

    def get_logger(self):
        return self.logger

# Initialization in settings or main module: ---------------------------------------------------------------------------
"""
import logging
from app.utils.module_logger import ModuleLogger
module_logger = ModuleLogger(module_name = 'APP_NAME', log_dir='LOGS_DIR', log_level=logging.DEBUG)
logger = module_logger.get_logger()

logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')

"""

# Using in other modules -----------------------------------------------------------------------------------------------
# Since ModuleLogger already configures the root logger (root_logger),
# there is no need to import logger from settings (or main).
# All modules will automatically pick up the configuration.
"""
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
"""
