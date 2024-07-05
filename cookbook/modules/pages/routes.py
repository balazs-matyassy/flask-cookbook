from flask import render_template

from cookbook.modules.pages import bp


@bp.route('/')
def home():
    return render_template('pages/home.html')
