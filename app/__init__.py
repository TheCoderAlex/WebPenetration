from celery import Celery
from flask import Flask
from config import config


def register_blueprint(app):
    from app.api import api
    from app.views import views
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(views)


app = Flask(__name__)
app.config.from_object(config['development'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

register_blueprint(app)
