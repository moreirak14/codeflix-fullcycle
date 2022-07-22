from datetime import datetime
from typing import Optional
import unittest
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category


class TestCategoryOutput(unittest.TestCase):

    def test_fields(self):
        self.assertEqual(CategoryOutput.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': bool,
            'created_at': datetime,
        })


class TestCategoryOutputMapper(unittest.TestCase):

    def test_to_output(self):
        category = Category(
            name="Movie",
            description="some description",
            is_active=True,
            created_at=datetime.now(),
        )
        output = CategoryOutputMapper.to_output(category=category)
        self.assertEqual(output, CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
        ))
