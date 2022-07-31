# pylint: disable=unexpected-keyword-arg no-member
import unittest
import pytest
from model_bakery import baker
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.infra.django.repositories import CategoryDjangoRepository
from core.category.infra.django.models import CategoryModel
from core.category.infra.django.mappers import CategoryModelMapper
from core.category.domain.entities import Category


@pytest.mark.django_db
class TestCategoryDjangoRepositoryUnit(unittest.TestCase):

    repo: CategoryDjangoRepository

    def setUp(self):
        self.repo = CategoryDjangoRepository()

    def test_insert(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, category.name)
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

        category = Category(
            name="Movies", description="some description", is_active=False
        )
        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, "Movies")
        self.assertEqual(model.description, "some description")
        self.assertFalse(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id("fake id")
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID: fake id"
        )

        unique_entity_id = UniqueEntityId("6eac08e5-5a54-4d2b-afeb-16253d0e75fb")
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID: 6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
        )

    def test_find_by_id(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        category_found = self.repo.find_by_id(category.id)
        self.assertEqual(category_found, category)

        category_found = self.repo.find_by_id(category.unique_entity_id)
        self.assertEqual(category_found, category)

    def test_find_all(self):
        models = baker.make(CategoryModel, _quantity=2)
        categories = self.repo.find_all()

        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0], CategoryModelMapper.to_entity(model=models[0]))
        self.assertEqual(categories[1], CategoryModelMapper.to_entity(model=models[1]))
