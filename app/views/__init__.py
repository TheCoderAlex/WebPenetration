from flask import Blueprint

views = Blueprint('views', __name__)

from app.views import index
from app.views import config
from app.views import hosts
