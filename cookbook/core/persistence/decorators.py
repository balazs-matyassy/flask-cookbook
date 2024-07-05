import functools

from flask import g


def scalar(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        return g.session.scalar(view(*args, **kwargs))

    return wrapped_view


def scalars(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        return g.session.scalars(view(*args, **kwargs))

    return wrapped_view
