from flask import Blueprint

bp = Blueprint('recipes', __name__)

from cookbook.modules.recipes import routes
