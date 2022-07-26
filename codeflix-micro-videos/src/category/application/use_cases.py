from dataclasses import asdict, dataclass
from typing import List, Optional
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
        return CategoryOutputMapper.to_output(category=category)

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
        return CategoryOutputMapper.to_output(category=category)

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
        return ListCategoryUseCase.Output(
            items=list(map(CategoryOutputMapper.to_output, result.items)),
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page,
        )

    @dataclass(slots=True, frozen=True)
    class Input:
        page: Optional[int] = None
        per_page: Optional[int] = None
        sort: Optional[str] = None
        sort_dir: Optional[str] = None
        filter: Optional[str] = None

    @dataclass(slots=True, frozen=True)
    class Output:
        items: List[CategoryOutput]
        total: int
        current_page: int
        per_page: int
        last_page: int
