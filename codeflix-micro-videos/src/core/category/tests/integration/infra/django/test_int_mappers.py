# pylint: disable=unexpected-keyword-arg
import unittest
import pytest
from django.utils import timezone
from core.category.infra.django.models import CategoryModel
from core.category.domain.entities import Category
from core.category.infra.django.mappers import CategoryModelMapper


@pytest.mark.django_db
class TestCategoryModelMapper(unittest.TestCase):
    def test_to_entity(self):
        created_at = timezone.now()
        model = CategoryModel(
            id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
            name="Movie",
            description="some description",
            is_active=True,
            created_at=created_at,
        )
        entity = CategoryModelMapper.to_entity(model=model)

        self.assertEqual(str(entity.id), "6eac08e5-5a54-4d2b-afeb-16253d0e75fb")
        self.assertEqual(entity.name, "Movie")
        self.assertEqual(entity.description, "some description")
        self.assertTrue(entity.is_active)
        self.assertEqual(entity.created_at, created_at)

    def test_to_model(self):
        entity = Category(
            name="Movie",
            description="some description",
            is_active=True,
        )
        model = CategoryModelMapper.to_model(entity=entity)

        self.assertEqual(str(model.id), entity.id)
        self.assertEqual(model.name, "Movie")
        self.assertEqual(model.description, "some description")
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, entity.created_at)
