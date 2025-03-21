from abc import ABC, abstractmethod
from src.domain.entities.balance import Balance


class BalanceRepository(ABC):
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Balance:
        pass

    @abstractmethod
    def get_amount(self, user_id: int) -> int:
        pass

    @abstractmethod
    def save(self, balance: Balance):
        pass
