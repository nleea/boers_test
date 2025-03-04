from src.application.auth_module.api.repositories.persons_repository import (
    PersonRepository,
)
from src.application.auth_module.api.repositories.user_repository import UserRepository
from src.application.auth_module.api.services.person_service import PersonService
from src.application.auth_module.api.services.user_service import UserService


class AuthModuleRepositoryFactory:

    @staticmethod
    def get_user_repository():
        return UserRepository()

    @staticmethod
    def get_person_repository():
        return PersonRepository()

    @staticmethod
    def get_user_service(serializer):
        repository = AuthModuleRepositoryFactory.get_user_repository()
        person_repository = AuthModuleRepositoryFactory.get_person_repository()
        return UserService(repository, serializer, person_repository)

    @staticmethod
    def get_person_service(serializer):
        repository = AuthModuleRepositoryFactory.get_person_repository()
        return PersonService(repository, serializer)
