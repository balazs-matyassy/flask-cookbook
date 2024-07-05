from flask import Blueprint

bp = Blueprint('pages', __name__)

from cookbook.modules.pages import routes
