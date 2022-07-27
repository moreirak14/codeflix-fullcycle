from dataclasses import asdict, dataclass
from typing import List, Optional
from __seedwork.application.dto import PaginationOutput, PaginationOutputMapper, SearchInput
from __seedwork.application.use_cases import UseCase
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: "Input") -> "Output":
        category = Category(**asdict(input_param))

        self.category_repo.insert(category)
        return self.__to_output(category=category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.from_child(CreateCategoryUseCase.Output).to_output(category=category)

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field("description").default
        is_active: Optional[bool] = Category.get_field("is_active").default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: "Input") -> "Output":
        category = self.category_repo.find_by_id(input_param.id)

        self.category_repo.insert(category)
        return self.__to_output(category=category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.from_child(GetCategoryUseCase.Output).to_output(category=category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: "Input") -> "Output":
        search_params = self.category_repo.SearchParams(**asdict(input_param))
        result = self.category_repo.search(search_params)
        return self.__to_output(result=result)

    def __to_output(self, result: CategoryRepository.SearchResult):
        items = list(
            map(CategoryOutputMapper.without_child().to_output, result.items)),
        return PaginationOutputMapper.from_child(output_child=ListCategoryUseCase.Output).to_output(items=items, result=result)

    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass

    @dataclass(slots=True, frozen=True)
    class Output(PaginationOutput[CategoryOutput]):
        pass
