from typing import List

from alchemical import Model
from sqlalchemy import Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cookbook.core.persistence.mixins import AuthoringMixin, FileMixin


class Recipe(Model, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    owned_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False, index=True)

    category: Mapped['Category'] = relationship(
        back_populates='recipes',
        foreign_keys='Recipe.category_id'
    )
    ingredients: Mapped[List['Ingredient']] = relationship(
        back_populates='recipe',
        order_by='asc(Ingredient.id)',
        cascade='all, delete-orphan'
    )
    images: Mapped[List['Image']] = relationship(
        back_populates='recipe',
        order_by='asc(Image.id)',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Recipe {self.name}>'


class Ingredient(Model, AuthoringMixin):
    __table_args__ = (
        UniqueConstraint('recipe_id', 'name'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit: Mapped[str] = mapped_column(String(180), nullable=False)

    recipe: Mapped['Recipe'] = relationship(
        back_populates='ingredients',
        foreign_keys='Ingredient.recipe_id'
    )

    def __repr__(self):
        return f'<Ingredient {self.recipe.name} - {self.name}>'


class Image(Model, FileMixin, AuthoringMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'), nullable=False, index=True)

    recipe: Mapped['Recipe'] = relationship(
        back_populates='images',
        foreign_keys='Image.recipe_id'
    )

    def __repr__(self):
        return f'<Image {self.recipe.name} - {self.filename}>'


