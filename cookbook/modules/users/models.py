from typing import List

from alchemical import Model
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from cookbook.core.persistence.mixins import AuthoringMixin


class Role(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)

    users: Mapped[List['User']] = relationship(
        back_populates='role',
        order_by='asc(User.username)'
    )

    def __repr__(self):
        return f'<Role {self.name}>'


class User(Model, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    digest: Mapped[str] = mapped_column('password', String(180), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=False, index=True)

    role: Mapped['Role'] = relationship(
        back_populates='users',
        foreign_keys='User.role_id'
    )

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        if value:
            self.digest = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.digest, password)

    def __repr__(self):
        return f'<User {self.username}>'
