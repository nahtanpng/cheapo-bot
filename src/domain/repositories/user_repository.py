from abc import ABC, abstractmethod
from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_last_daily(self, user_id: int) -> str:
        pass

    @abstractmethod
    def set_last_daily(self, user_id: int, date: str):
        pass

    @abstractmethod
    def save(self, user: User):
        pass
