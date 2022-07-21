from typing import Optional
import unittest
from unittest.mock import patch
from category.application.use_cases import CreateCategoryUseCase
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):

    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_input(self):
        self.assertEqual(self.use_case.Input.__annotations__, {
            "name": str,
            "description": Optional[str],
            "is_active": Optional[bool],
        })

        description_field_default = self.use_case.Input.__dataclass_fields__[
            "description"].default
        self.assertEqual(description_field_default,
                         Category.get_field("description").default)

        is_active_default = self.use_case.Input.__dataclass_fields__[
            "is_active"].default
        self.assertEqual(is_active_default,
                         Category.get_field("is_active").default)

    def test_execute(self):
        with patch.object(self.category_repo, "insert", wraps=self.category_repo.insert) as spy_insert:
            input_param = self.use_case.Input(name="Movie")
            output = self.use_case.execute(input_param=input_param)
            spy_insert.assert_called_once()

            self.assertEqual(output, self.use_case.Output(
                id=self.category_repo.items[0].id,
                name="Movie",
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at,
            ))

            input_param = self.use_case.Input(
                name="Movie", description="some description", is_active=True)
            output = self.use_case.execute(input_param=input_param)

            self.assertEqual(output, self.use_case.Output(
                id=self.category_repo.items[1].id,
                name="Movie",
                description="some description",
                is_active=True,
                created_at=self.category_repo.items[1].created_at,
            ))

            input_param = self.use_case.Input(
                name="Movie", description="some description", is_active=False)
            output = self.use_case.execute(input_param=input_param)

            self.assertEqual(output, self.use_case.Output(
                id=self.category_repo.items[2].id,
                name="Movie",
                description="some description",
                is_active=False,
                created_at=self.category_repo.items[2].created_at,
            ))
