from abc import abstractmethod
from src.domain.response_handlrer import ServiceMeta


class BaseService(metaclass=ServiceMeta):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, pk):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
