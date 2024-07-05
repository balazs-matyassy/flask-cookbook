from flask import Flask
from flask_wtf import CSRFProtect

import cookbook.core.persistence
import cookbook.core.security
import cookbook.modules.categories
import cookbook.modules.pages
import cookbook.modules.recipes
import cookbook.modules.security
import cookbook.modules.users
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    csrf = CSRFProtect()
    csrf.init_app(app)

    cookbook.core.persistence.init_app(app)
    cookbook.core.security.init_app(app)

    app.register_blueprint(cookbook.modules.categories.bp, url_prefix='/categories')
    app.register_blueprint(cookbook.modules.pages.bp, url_prefix='/')
    app.register_blueprint(cookbook.modules.recipes.bp, url_prefix='/recipes')
    app.register_blueprint(cookbook.modules.security.bp, url_prefix='/')
    app.register_blueprint(cookbook.modules.users.bp, url_prefix='/users')

    return app


if __name__ == '__main__':
    create_app().run()
