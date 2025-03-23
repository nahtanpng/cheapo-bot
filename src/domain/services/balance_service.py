from datetime import datetime, timedelta

from src.domain.repositories.balance_repository import BalanceRepository
from src.domain.repositories.user_repository import UserRepository


class BalanceService:
    def __init__(self, balance_repository: BalanceRepository, user_repository: UserRepository):
        self.balance_repository = balance_repository
        self.user_repository = user_repository

    def get_amount(self, user_id: int):
        balance = self.balance_repository.get_amount(user_id)

        return balance

    def get_daily(self, user_id: int) -> tuple[bool, int]:
        reward = 100

        last_daily = self.user_repository.get_last_daily(user_id)
        if last_daily:
            last_daily_date = datetime.fromisoformat(last_daily)
            if datetime.now() - last_daily_date < timedelta(days=1):
                return False, 0

        self.balance_repository.update_balance(user_id, reward)
        self.user_repository.set_last_daily(user_id, datetime.now().isoformat())

        return True, reward