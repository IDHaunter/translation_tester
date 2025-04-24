from flask import Flask, request, Blueprint
from app.settings import APP_NAME, APP_VER, AUTHORIZE
from app.routes.common.responses import ResponseMessages

root_blueprint = Blueprint('root_blueprint', __name__)

# ------------------------------------------------------/logs-----------------------------------------------------------
@root_blueprint.route('/', methods=['GET'])
def root():
    try:
        return f'''
            <html>
                <head>
                    <title>Welcome to the {APP_NAME} service!</title>
                </head>
                <body>
                    <h1>Welcome to the {APP_NAME} service!</h1>
                    <p>version : {APP_VER['ver']} </p>
                    <p>date : {APP_VER['date']} </p>
                    <p>info : {APP_VER['info']} </p>
                    <p>authorization: <span style="color: blue;">{AUTHORIZE}</span></p>
                    <p>                  </p>
                    <p>List of protected endpoints:</p>
                    <ul>
                        <li>/logs</li>
                        <li>...</li>
                    </ul>
                </body>
            </html>
            '''
    except Exception as e:
        return ResponseMessages.error_500(f"{e}")


