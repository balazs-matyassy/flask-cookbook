import functools

from flask import g, abort


def is_granted(*roles):
    roles = [arg.upper() for arg in roles]

    def is_granted_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if (not g.user
                    or ('IS_AUTHENTICATED_FULLY' not in roles
                        and 'ROLE_' + g.user.role.name not in roles)):
                abort(401)

            return view(*args, **kwargs)

        return wrapped_view

    return is_granted_decorator
