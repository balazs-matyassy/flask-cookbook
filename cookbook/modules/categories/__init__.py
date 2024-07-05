from flask import Blueprint

bp = Blueprint('categories', __name__)

from cookbook.modules.categories import routes
