from src.domain.services.balance_service import BalanceService


class BalanceUseCase:
    def __init__(self, balance_service: BalanceService):
        self.balance_service = balance_service

    def get_amount(self, user_id: int):
        return self.balance_service.get_amount(user_id)