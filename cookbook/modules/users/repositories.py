from cookbook.core.persistence.decorators import scalars, scalar
from cookbook.core.persistence.repository import CrudRepository


class RoleRepository(CrudRepository):
    @staticmethod
    @scalar
    def find_by_name(name):
        return (
            Role
            .select()
            .where(Role.name == name)
        )

    @staticmethod
    def _model():
        return Role

    @staticmethod
    def _default_sort_key():
        return Role.name


class UserRepository(CrudRepository):
    @staticmethod
    @scalar
    def find_by_username(username):
        return (
            User
            .select()
            .where(User.username == username)
        )

    @staticmethod
    @scalars
    def find_all_by_username_like(username):
        return (
            User
            .select()
            .join(Role)
            .where(User.username.like(f'%{username}%'))
            .order_by(Role.name, User.username)
        )

    @staticmethod
    def _model():
        return User

    @staticmethod
    def _default_sort_key():
        return User.username


from cookbook.modules.users.models import User, Role
