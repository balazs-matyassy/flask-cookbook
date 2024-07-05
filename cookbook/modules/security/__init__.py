from flask import Blueprint

bp = Blueprint('security', __name__)

from cookbook.modules.security import routes
