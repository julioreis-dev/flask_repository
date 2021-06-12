from flask import Blueprint

login = Blueprint('logins', __name__)

from . import views
