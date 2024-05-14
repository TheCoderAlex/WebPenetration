from flask import Blueprint

views = Blueprint('views', __name__)

from app.views import index
