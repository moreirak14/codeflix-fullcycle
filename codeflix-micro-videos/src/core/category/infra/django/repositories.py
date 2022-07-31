# pylint: disable=no-member unexpected-keyword-arg
from typing import List
from django.core import exceptions as django_exceptions
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django.models import CategoryModel
from core.category.infra.django.mappers import CategoryModelMapper


class CategoryDjangoRepository(CategoryRepository):
    def insert(self, entity: Category) -> None:
        model = CategoryModelMapper.to_model(entity=entity)
        model.save()

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Category:
        id_str = str(entity_id)
        model = self._get(entity_id=id_str)
        return CategoryModelMapper.to_entity(model=model)

    def find_all(self) -> List[Category]:
        return [
            CategoryModelMapper.to_entity(model=model)
            for model in CategoryModel.objects.all()
        ]

    def update(self, entity: Category) -> None:
        raise NotImplementedError()

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedError()

    def search(
        self, input_params: CategoryRepository.SearchParams
    ) -> CategoryRepository.SearchResult:
        raise NotImplementedError()

    def _get(self, entity_id: str) -> CategoryModel:
        try:
            return CategoryModel.objects.get(pk=entity_id)
        except (
            CategoryModel.DoesNotExist,
            django_exceptions.ValidationError,
        ) as exception:
            raise NotFoundException(
                f"Entity not found using ID: {entity_id}"
            ) from exception
