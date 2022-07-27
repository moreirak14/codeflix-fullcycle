from datetime import datetime, timedelta
from typing import Optional
import unittest
from unittest.mock import patch
from __seedwork.domain.exceptions import NotFoundException
from __seedwork.application.use_cases import UseCase
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase, ListCategoryUseCase
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):

    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_if_instance_an_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

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

    def test_output(self):
        self.assertTrue(issubclass(self.use_case.Output, CategoryOutput))

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


class TestGetCategoryUseCaseUnit(unittest.TestCase):

    use_case: GetCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)

    def test_if_instance_an_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(self.use_case.Input.__annotations__, {
            "id": str,
        })

    def test_output(self):
        self.assertTrue(issubclass(self.use_case.Output, CategoryOutput))

    def test_throws_exception_when_category_not_found(self):
        input_param = self.use_case.Input("fake id")
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param=input_param)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID: fake id")

    def test_execute(self):
        category = Category(name="Movie")
        self.category_repo.items = [category]

        with patch.object(self.category_repo, "find_by_id", wraps=self.category_repo.find_by_id) as spy_find_by_id:
            input_param = self.use_case.Input(category.id)
            output = self.use_case.execute(input_param=input_param)
            spy_find_by_id.assert_called_once()

            self.assertEqual(output, self.use_case.Output(
                id=self.category_repo.items[0].id,
                name="Movie",
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at,
            ))


class TestListCategoryUseCaseUnit(unittest.TestCase):

    use_case: ListCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = ListCategoryUseCase(self.category_repo)

    def test_if_instance_an_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_execute_using_empty_search_params(self):
        self.category_repo.items = [
            Category(name="teste 1"),
            Category(name="teste 2", created_at=datetime.now() +
                     timedelta(seconds=200)),
        ]
        with patch.object(self.category_repo, "search", wraps=self.category_repo.search) as spy_search:
            input_param = self.use_case.Input()
            output = self.use_case.execute(input_param=input_param)
            spy_search.assert_called_once()

            self.assertEqual(output, self.use_case.Output(
                items=list(map(CategoryOutputMapper.to_output,
                           self.category_repo.items[::-1])),
                total=2,
                current_page=1,
                per_page=15,
                last_page=1,
            ))

    def test_execute_using_pagination_and_sort_and_filter(self):
        items = [
            Category(name="a"),
            Category(name="AAA"),
            Category(name="AaA"),
            Category(name="b"),
            Category(name="c"),
        ]
        self.category_repo.items = items

        input_param = self.use_case.Input(
            page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="a"
        )
        output = self.use_case.execute(input_param=input_param)
        self.assertEqual(output, self.use_case.Output(
            items=list(map(CategoryOutputMapper.to_output,
                           [items[1], items[2]])),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2,
        ))

        input_param = self.use_case.Input(
            page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="a"
        )
        output = self.use_case.execute(input_param=input_param)
        self.assertEqual(output, self.use_case.Output(
            items=list(map(CategoryOutputMapper.to_output,
                           [items[0]])),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2,
        ))

        input_param = self.use_case.Input(
            page=1,
            per_page=2,
            sort="name",
            sort_dir="desc",
            filter="a"
        )
        output = self.use_case.execute(input_param=input_param)
        self.assertEqual(output, self.use_case.Output(
            items=list(map(CategoryOutputMapper.to_output,
                           [items[0], items[2]])),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2,
        ))
