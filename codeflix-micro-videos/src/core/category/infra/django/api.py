from dataclasses import asdict, dataclass
from typing import Callable
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoryUseCase,
)

@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoryUseCase]

    def post(self, request: Request):
        input_param = CreateCategoryUseCase.Input(**request.data)
        output = self.create_use_case().execute(input_param=input_param)
        return Response(asdict(output), status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        input_param = ListCategoryUseCase.Input(**request.query_params.dict())
        output = self.list_use_case().execute(input_param=input_param)
        return Response(asdict(output), status=status.HTTP_200_OK)
