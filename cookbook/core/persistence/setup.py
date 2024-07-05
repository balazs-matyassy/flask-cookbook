def install():
    db.drop_all()
    db.create_all()

    with db.Session() as session:
        role_admin = Role(name='ADMIN')
        session.add(role_admin)

        role_moderator = Role(name='MODERATOR')
        session.add(role_moderator)

        role_editor = Role(name='EDITOR')
        session.add(role_editor)

        role_user = Role(name='USER')
        session.add(role_user)

        user = User()
        user.username = 'admin'
        user.password = 'Admin123.'
        user.role = role_admin
        session.add(user)

        session.commit()


from cookbook.core.persistence import db
from cookbook.modules.users.models import Role, User
