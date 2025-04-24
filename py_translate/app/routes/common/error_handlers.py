from flask import Flask
from app.routes.common.responses import ResponseMessages

def register_error_handlers(app: Flask):
    # Register new default error handlers in Flask.
    @app.errorhandler(400)
    def handle_400(error):
        return ResponseMessages.error_400(str(error))

    @app.errorhandler(401)
    def handle_401(error):
        return ResponseMessages.error_401(str(error))

    @app.errorhandler(403)
    def handle_403(error):
        return ResponseMessages.error_403(str(error))

    @app.errorhandler(404)
    def handle_404(error):
        return ResponseMessages.error_404(str(error))

    @app.errorhandler(500)
    def handle_500(error):
        return ResponseMessages.error_500(str(error))
