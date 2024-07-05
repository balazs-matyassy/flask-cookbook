from flask import g, session, redirect, url_for, request

from cookbook.modules.users.repositories import UserRepository


def init_app(app):
    app.before_request(__load_current_user)
    app.register_error_handler(401, __handle_unauthorized)

    app.jinja_env.globals['is_granted'] = __is_granted
    app.jinja_env.globals['is_owner_or_granted'] = __is_owner_or_granted


def __load_current_user():
    if not session.get('user_id'):
        g.user = None
    else:
        g.user = UserRepository.find_by_id(session.get('user_id'))


def __handle_unauthorized(e):
    if not g.user:
        return redirect(url_for('security.login', redirect=request.path))

    return e


def __is_granted(*roles):
    roles = [arg.upper() for arg in roles]

    return (g.user
            and ('IS_AUTHENTICATED_FULLY' in roles
                 or 'ROLE_' + g.user.role.name in roles))


def __is_owner_or_granted(entity, *roles):
    roles = [arg.upper() for arg in roles]

    return (g.user
            and (entity.owned_by == g.user.id
                 or 'IS_AUTHENTICATED_FULLY' in roles
                 or 'ROLE_' + g.user.role.name in roles))
