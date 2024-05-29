from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import ping
from app.api import tasks
from app.api import config
from app.api import hosts
from app.api import files
from app.api import check