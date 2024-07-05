import click
from alchemical.flask import Alchemical
from flask import g


db = Alchemical()


def init_app(app):
    app.before_request(__create_session)
    app.teardown_appcontext(__close_session)
    app.cli.add_command(__install_command)

    db.init_app(app)


def __create_session():
    if 'session' not in g:
        g.session = db.Session()


def __close_session(e):
    if 'session' in g:
        g.pop('session').close()


@click.command('install')
def __install_command():
    install()

    click.echo('Application installation successful.')


from cookbook.core.persistence.setup import install
