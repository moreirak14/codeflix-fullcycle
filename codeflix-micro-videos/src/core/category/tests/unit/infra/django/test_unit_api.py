from datetime import datetime
import unittest
from unittest import mock
from core.category.application.dto import CategoryOutput
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoryUseCase,
    UpdateCategoryUseCase,
)
from core.category.infra.django.api import CategoryResource


class TestCategoryResourceUnit(unittest.TestCase):
    def __init_all_none(self):
        return {
            "list_use_case": None,
            "create_use_case": None,
            "get_use_case": None,
            "update_use_case": None,
            "delete_use_case": None,
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
            **{
                **self.__init_all_none(),
                "create_use_case": lambda: mock_create_use_case,
            }
        )
        send_data = {"name": "Movie"}
        _request = APIRequestFactory().post(path="/", data=send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.post(request=request)

        mock_create_use_case.execute.assert_called_with(
            input_param=CreateCategoryUseCase.Input(name="Movie")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                "name": "Movie",
                "description": None,
                "is_active": True,
                "created_at": mock_create_use_case.execute.return_value.created_at,
            },
        )

    def test_get_method(self):
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
            last_page=1,
        )

        resource = CategoryResource(
            **{**self.__init_all_none(), "list_use_case": lambda: mock_list_use_case}
        )
        path_data = "/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test"
        _request = APIRequestFactory().get(path=path_data)
        request = Request(_request)
        response = resource.get(request=request)

        mock_list_use_case.execute.assert_called_with(
            input_param=ListCategoryUseCase.Input(
                page="1", per_page="1", sort="name", sort_dir="asc", filter="test"
            )
        )
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
                        "created_at": mock_list_use_case.execute.return_value.items[
                            0
                        ].created_at,
                    }
                ],
                "total": 1,
                "current_page": 1,
                "per_page": 2,
                "last_page": 1,
            },
        )

    def test_if_get_invoke_get_object(self):
        mock_list_use_case = mock.Mock(ListCategoryUseCase)
        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
            name="Movie",
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                "list_use_case": lambda: mock_list_use_case,
                "get_use_case": lambda: mock_get_use_case,
            }
        )
        response = resource.get(None, id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb")

        mock_get_use_case.execute.assert_called_with(
            input_param=GetCategoryUseCase.Input(
                id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb"
            )
        )
        self.assertEqual(mock_list_use_case.call_count, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                "name": "Movie",
                "description": None,
                "is_active": True,
                "created_at": mock_get_use_case.execute.return_value.created_at,
            },
        )

    def test_get_object_method(self):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
            name="Movie",
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{**self.__init_all_none(), "get_use_case": lambda: mock_get_use_case}
        )
        response = resource.get_object(id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb")

        mock_get_use_case.execute.assert_called_with(
            input_param=GetCategoryUseCase.Input(
                id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb"
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                "name": "Movie",
                "description": None,
                "is_active": True,
                "created_at": mock_get_use_case.execute.return_value.created_at,
            },
        )

    def test_put_object_method(self):
        mock_put_use_case = mock.Mock(UpdateCategoryUseCase)
        mock_put_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
            name="Movie",
            description=None,
            is_active=True,
            created_at=datetime.now(),
        )

        resource = CategoryResource(
            **{**self.__init_all_none(), "update_use_case": lambda: mock_put_use_case}
        )
        send_data = {"id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb", "name": "Movie"}
        _request = APIRequestFactory().put(path="/", data=send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.put(
            request=send_data, id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb"
        )

        mock_put_use_case.execute.assert_called_with(
            input_param=UpdateCategoryUseCase.Input(
                id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                name="Movie",
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                "name": "Movie",
                "description": None,
                "is_active": True,
                "created_at": mock_put_use_case.execute.return_value.created_at,
            },
        )

    def test_delete_object_method(self):
        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                "delete_use_case": lambda: mock_delete_use_case,
            }
        )
        _request = APIRequestFactory().delete(path="/")
        request = Request(_request)
        response = resource.delete(
            _request=request, id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb"
        )
        mock_delete_use_case.execute.assert_called_with(
            input_param=DeleteCategoryUseCase.Input(
                id="6eac08e5-5a54-4d2b-afeb-16253d0e75fb"
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
