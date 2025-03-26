import random

from src.domain.repositories.balance_repository import BalanceRepository
from src.domain.repositories.gambling_repository import GamblingRepository


class GamblingService:
    def __init__(self, balance_repository: BalanceRepository, gambling_repository: GamblingRepository):
        self.balance_repository = balance_repository
        self.gambling_repository = gambling_repository

    def flip(self, user_id: int, side: str, amount: int):
        user_balance = self.balance_repository.find_by_user_id(user_id)

        if user_balance.amount < amount:
            raise ValueError(user_balance.amount)

        coin_faces = ["heads", "tails"]
        chosen_face = random.choice(coin_faces)

        if side == chosen_face:
            self.gambling_repository.flip_reward(user_id, amount, is_winner=True)
            return True, chosen_face
        else:
            self.gambling_repository.flip_reward(user_id, amount, is_winner=False)
            return False, chosen_face
