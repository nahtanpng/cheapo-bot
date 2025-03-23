from abc import ABC, abstractmethod
from src.domain.entities.balance import Balance


class GamblingRepository(ABC):
    @abstractmethod
    def flip_reward(self, user_id: int, value: int, is_winner: bool):
        pass