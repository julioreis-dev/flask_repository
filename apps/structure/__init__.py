from flask import Blueprint

coin = Blueprint('coin', __name__)

from . import views