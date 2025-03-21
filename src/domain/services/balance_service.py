from src.domain.repositories.balance_repository import BalanceRepository

class BalanceService:
    def __init__(self, balance_repository: BalanceRepository):
        self.balance_repository = balance_repository

    def get_amount(self, user_id: int):
        balance = self.balance_repository.get_amount(user_id)

        return balance