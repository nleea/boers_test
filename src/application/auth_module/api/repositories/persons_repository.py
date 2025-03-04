from src.interfaces.repository.base_repository import BaseRepository
from src.application.auth_module.models.auth_models import Person

class PersonRepository (BaseRepository):
    
    def __init__(self) -> None:
        super().__init__(Person)