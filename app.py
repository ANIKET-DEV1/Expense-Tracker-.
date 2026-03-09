from flask import Flask,session

def create_app():
    app = Flask(__name__)
    app.secret_key="AnikEtG12W3Rm"
    # app.config["SECRETKEY"]

    from .views import view,auth
    app.register_blueprint(view)
    app.register_blueprint(auth)

    return app