from dataclasses import asdict
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoryUseCase,
)
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository


class CategoryResource(APIView):

    repo = CategoryInMemoryRepository()

    def post(self, request: Request):
        create_use_case = CreateCategoryUseCase(self.repo)
        input_param = CreateCategoryUseCase.Input(name=request.data["name"])
        output = create_use_case.execute(input_param=input_param)
        return Response(asdict(output))

    def get(self, request: Request):
        list_use_case = ListCategoryUseCase(self.repo)
        input_param = ListCategoryUseCase.Input()
        output = list_use_case.execute(input_param=input_param)
        return Response(asdict(output))


# @api_view(["POST"])
# def hello_world(request: Request):
#     create_use_case = CreateCategoryUseCase(CategoryInMemoryRepository())
#     input_param = CreateCategoryUseCase.Input(name=request.data["name"])
#     output = create_use_case.execute(input_param=input_param)
#     return Response(asdict(output))
