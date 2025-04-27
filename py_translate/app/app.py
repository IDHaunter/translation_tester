import logging
from flask import Flask
from app.settings import (LOGS_DIR, APP_NAME, APP_VER, AUTHORIZE,
                         DEBUG, PORT, HOST)
from app.routes.common.error_handlers import register_error_handlers
from app.routes.root import root_blueprint
from app.routes.logs import logs_blueprint
from app.routes.translate import translate_blueprint
from app.middleware import check_authorization

app = Flask(__name__)

logger = logging.getLogger(__name__)

logger.info(f"------ START : {APP_NAME.upper()}")
logger.info(f"     version : {APP_VER['ver']}")
logger.info(f"        date : {APP_VER['date']}")
logger.info(f"        info : {APP_VER['info']}")

logger.info(f"Debug: {DEBUG}")
logger.info(f"Server port: {PORT}")
logger.info(f"Server host: {HOST}")
logger.info(f"Authorization: {AUTHORIZE}")

register_error_handlers(app) # Register error handlers

app.register_blueprint(root_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(translate_blueprint)

app.before_request(check_authorization) # Register the middleware function globally

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host=HOST)
