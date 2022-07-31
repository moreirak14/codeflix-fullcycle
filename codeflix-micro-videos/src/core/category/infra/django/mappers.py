# pylint: disable=no-member unexpected-keyword-arg
from core.__seedwork.domain.exceptions import (
    EntityValidationException,
    LoadEntityException,
)
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.infra.django.models import CategoryModel


class CategoryModelMapper:
    @staticmethod
    def to_entity(model: CategoryModel) -> Category:
        try:
            return Category(
                unique_entity_id=UniqueEntityId(id=model.id),
                name=model.name,
                description=model.description,
                is_active=model.is_active,
                created_at=model.created_at,
            )
        except EntityValidationException as exception:
            raise LoadEntityException(exception.error) from exception

    @staticmethod
    def to_model(entity: Category) -> CategoryModel:
        return CategoryModel(**entity.to_dict())
