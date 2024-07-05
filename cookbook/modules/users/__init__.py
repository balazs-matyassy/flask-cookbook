from flask import Blueprint

bp = Blueprint('users', __name__)

from cookbook.modules.users import routes
