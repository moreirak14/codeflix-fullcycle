from django.urls import path
from django_app import container
from core.category.application.use_cases import CreateCategoryUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from .api import CategoryResource


class CategoryInMemoryRepositoryFactory:

    repo: CategoryInMemoryRepository = None

    @classmethod
    def create(cls):
        if not cls.repo:
            cls.repo = CategoryInMemoryRepository()
        return cls.repo


class CreateCategoryUseCaseFactory:

    @staticmethod
    def create():
        repo = CategoryInMemoryRepositoryFactory.create()
        return CreateCategoryUseCase(repo)


urlpatterns = [
    path("categories/", CategoryResource.as_view(
        create_use_case=container.use_case_category_create_category
    ))]
