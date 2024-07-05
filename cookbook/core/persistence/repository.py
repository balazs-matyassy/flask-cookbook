from abc import ABC, abstractmethod
from datetime import datetime

from flask import g

from cookbook.core.persistence.decorators import scalars


class CrudRepository(ABC):
    @classmethod
    @scalars
    def find_all(cls):
        if cls._default_sort_key:
            return (
                cls._model()
                .select()
                .order_by(cls._default_sort_key())
            )
        else:
            return (
                cls._model()
                .select()
            )

    @classmethod
    def find_by_id(cls, entity_id):
        return g.session.get(cls._model(), entity_id)

    @staticmethod
    def save(entity):
        now = datetime.utcnow()

        if not entity.id:
            if hasattr(entity, 'created_at'):
                entity.created_at = now

            if hasattr(entity, 'created_by'):
                entity.created_by = g.user.id

        if hasattr(entity, 'modified_at'):
            entity.modified_at = now

        if hasattr(entity, 'modified_by'):
            entity.modified_by = g.user.id

        if not entity.id:
            g.session.add(entity)

        try:
            g.session.commit()
        except Exception as err:
            g.session.rollback()
            raise err

        return entity

    @staticmethod
    def delete(entity):
        g.session.delete(entity)

        try:
            g.session.commit()
        except Exception as err:
            g.session.rollback()
            raise err

    @staticmethod
    @abstractmethod
    def _model():
        raise NotImplementedError()

    @staticmethod
    def _default_sort_key():
        return None
