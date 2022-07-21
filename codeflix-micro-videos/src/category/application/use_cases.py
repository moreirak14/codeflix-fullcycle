from dataclasses import asdict, dataclass
from typing import Optional
from category.application.dto import CategoryOutput
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase:

    category_repo: CategoryRepository

    def execute(self, input_param: "Input") -> "Output":
        category = Category(**asdict(input_param))

        self.category_repo.insert(category)
        return self.Output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
        )

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field("description").default
        is_active: Optional[bool] = Category.get_field("is_active").default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase:

    category_repo: CategoryRepository

    def execute(self, input_param: "Input") -> "Output":
        category = self.category_repo.find_by_id(input_param.id)

        self.category_repo.insert(category)
        return self.Output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
        )

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass
