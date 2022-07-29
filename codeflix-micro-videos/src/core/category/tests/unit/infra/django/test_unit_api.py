from datetime import datetime
import unittest
from unittest import mock
from core.category.application.dto import CategoryOutput
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.category.application.use_cases import CreateCategoryUseCase, ListCategoryUseCase
from core.category.infra.django.api import CategoryResource


class TestCategoryResourceUnit(unittest.TestCase):

    def __init_all_none(self):
        return {
            "list_use_case": None,
            "create_use_case": None
        }

    def test_post_method(self):
        mock_create_use_case = mock.Mock(CreateCategoryUseCase)
        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
            name="Movie",
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{**self.__init_all_none(), "create_use_case": lambda: mock_create_use_case})
        send_data = {"name": "Movie"}
        _request = APIRequestFactory().post(path="/", data=send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.post(request=request)

        mock_create_use_case.execute.assert_called_with(
            input_param=CreateCategoryUseCase.Input(name="Movie"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
            "name": "Movie",
            "description": None,
            "is_active": True,
            "created_at": mock_create_use_case.execute.return_value.created_at,
        })

    def test_list_method(self):
        mock_list_use_case = mock.Mock(CreateCategoryUseCase)
        mock_list_use_case.execute.return_value = ListCategoryUseCase.Output(
            items=[
                CategoryOutput(
                    id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                    name="Movie",
                    description=None,
                    is_active=True,
                    created_at=datetime.now(),
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )

        resource = CategoryResource(
            **{**self.__init_all_none(), "list_use_case": lambda: mock_list_use_case})
        path_data = "/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test"
        _request = APIRequestFactory().get(path=path_data)
        request = Request(_request)
        response = resource.get(request=request)

        mock_list_use_case.execute.assert_called_with(input_param=ListCategoryUseCase.Input(
            page="1",
            per_page="1",
            sort="name",
            sort_dir="asc",
            filter="test"
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "items": [
                    {
                        "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                        "name": "Movie",
                        "description": None,
                        "is_active": True,
                        "created_at": mock_list_use_case.execute.return_value.items[0].created_at,
                    }
                ],
                "total": 1,
                "current_page": 1,
                "per_page": 2,
                "last_page": 1
            },)
