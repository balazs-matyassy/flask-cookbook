from cookbook.core.persistence.decorators import scalars, scalar
from cookbook.core.persistence.repository import CrudRepository


class RecipeRepository(CrudRepository):
    @staticmethod
    @scalars
    def find_all_by_name_like(name):
        return (
            Recipe
            .select()
            .join(Category)
            .where(Recipe.name.like(f'%{name}%'))
            .order_by(Category.name, Recipe.name)
        )

    @staticmethod
    def _model():
        return Recipe

    @staticmethod
    def _default_sort_key():
        return Recipe.name


class IngredientRepository(CrudRepository):
    @staticmethod
    @scalar
    def find_by_id_and_recipe_id(ingredient_id, recipe_id):
        return (
            Ingredient
            .select()
            .where(Ingredient.id == ingredient_id, Ingredient.recipe_id == recipe_id)
        )

    @staticmethod
    def _model():
        return Ingredient


class ImageRepository(CrudRepository):
    @staticmethod
    @scalar
    def find_by_id_and_recipe_id(image_id, recipe_id):
        return (
            Image
            .select()
            .where(Image.id == image_id, Image.recipe_id == recipe_id)
        )

    @staticmethod
    def _model():
        return Image


from cookbook.modules.categories.models import Category
from cookbook.modules.recipes.models import Recipe, Ingredient, Image
