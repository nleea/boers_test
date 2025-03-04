from src.application.auth_module.api.repositories.persons_repository import (
    PersonRepository,
)
from src.infrastructure.base_service import BaseService


class PersonService(BaseService):

    def __init__(self, repository: PersonRepository, serializer) -> None:
        self.repository = repository
        self.serializer = serializer

    def get_all(self):
        return self.serializer(self.repository.get_all(), many=True).data

    def get_by_id(self, pk):
        return self.serializer(self.repository.get_by_id(pk)).data

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
