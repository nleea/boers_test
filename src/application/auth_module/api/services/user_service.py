from src.application.auth_module.api.repositories.user_repository import UserRepository
from src.infrastructure.base_service import BaseService
from src.application.auth_module.api.repositories.persons_repository import PersonRepository
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class UserService(BaseService):
    def __init__(self, repository: UserRepository, serializer, person_repository: PersonRepository) -> None:
        self.repository = repository
        self.serializer = serializer
        self.person_repository = person_repository

    def get_all(self):
        """Obtiene todos los usuarios serializados"""
        users = self.repository.get_all().select_related("person")
        return self.serializer(users, many=True).data

    def get_by_id(self, pk):
        """Obtiene un usuario por ID"""
        user = self.repository.get_by_id(pk)
        if not user:
            raise ObjectDoesNotExist(f"Usuario con ID {pk} no encontrado.")
        return self.serializer(user).data

    @transaction.atomic
    def create(self, data):
        """Crea un usuario y su respectiva persona"""
        person_data = data.pop("person", None)
        if not person_data:
            raise ValueError("El campo 'person' es obligatorio.")

        person = self.person_repository.create(person_data)
        data["person_id"] = person.id
        data["email"] = person.email

        user = self.repository.create(data)
        return self.serializer(user).data

    @transaction.atomic
    def update(self, pk, data):
        """Actualiza un usuario por ID"""
        user = self.repository.get_by_id(pk)
        if not user:
            raise ObjectDoesNotExist(f"Usuario con ID {pk} no encontrado.")

        if "person" in data:
            person_data = data.pop("person")
            self.person_repository.update(user.person.id, person_data)

        user = self.repository.update(pk, data)
        return self.serializer(user).data

    @transaction.atomic
    def delete(self, pk):
        """Elimina un usuario por ID"""
        user = self.repository.get_by_id(pk)

        if not user:
            raise ObjectDoesNotExist(f"Usuario con ID {pk} no encontrado.")

        self.repository.delete(pk)
        self.person_repository.delete(user.person.id)
        return {"message": f"Usuario con ID {pk} eliminado correctamente."}

    def get_by_email(self, email):
        return self.repository.filter_custom(email=email).first()
    
    def get_by_token(self, token):
        return self.repository.filter_custom(token=token).first()