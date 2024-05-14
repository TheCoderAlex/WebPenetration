from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
