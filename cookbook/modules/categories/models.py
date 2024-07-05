from typing import List

from alchemical import Model
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cookbook.core.persistence.mixins import AuthoringMixin


class Category(Model, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    recipes: Mapped[List['Recipe']] = relationship(
        back_populates='category',
        order_by='asc(Recipe.name)'
    )

    def __repr__(self):
        return f'<Category {self.name}>'


