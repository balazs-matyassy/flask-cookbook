from cookbook.core.persistence.decorators import scalars
from cookbook.core.persistence.repository import CrudRepository


class CategoryRepository(CrudRepository):
    @staticmethod
    @scalars
    def find_all_by_name_like(name):
        return (
            Category
            .select()
            .where(Category.name.like(f'%{name}%'))
            .order_by(Category.name)
        )

    @staticmethod
    def _model():
        return Category

    @staticmethod
    def _default_sort_key():
        return Category.name


from cookbook.modules.categories.models import Category
