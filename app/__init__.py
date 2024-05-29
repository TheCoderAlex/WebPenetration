from celery import Celery
from flask import Flask
from config import config
from flask_cors import CORS


def register_blueprint(app):
    from app.api import api
    from app.views import views
    app.register_blueprint(api, url_prefix='/api')
    # 前端使用Vue.js，所以不需要使用Flask的模板引擎
    # app.register_blueprint(views)


app = Flask(__name__)
CORS(app, resource={r"/api/*": {"origins": "http://localhost:5173"}})
app.config.from_object(config['development'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

register_blueprint(app)
