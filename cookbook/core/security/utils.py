from flask import g, abort


def deny_access_unless_granted(*roles):
    roles = [arg.upper() for arg in roles]

    if (not g.user
            or ('IS_AUTHENTICATED_FULLY' not in roles
                and 'ROLE_' + g.user.role.name not in roles)):
        abort(401)


def deny_access_unless_owner_or_granted(entity, *roles):
    roles = [arg.upper() for arg in roles]

    if (not g.user
            or (entity.owned_by != g.user.id
                and 'IS_AUTHENTICATED_FULLY' not in roles
                and 'ROLE_' + g.user.role.name not in roles)):
        abort(401)
