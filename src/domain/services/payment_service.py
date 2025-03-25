from src.domain.repositories.balance_repository import BalanceRepository
from src.domain.repositories.user_repository import UserRepository


class PaymentService:
    def __init__(self, balance_repository: BalanceRepository):
        self.balance_repository = balance_repository

    def transfer(self, sender_id: int, receiver_id: int, amount: int):
        sender_balance = self.balance_repository.find_by_user_id(sender_id)
        receiver_balance = self.balance_repository.find_by_user_id(receiver_id)

        if sender_balance.amount < amount:
            raise ValueError("Insufficient Balance")

        sender_balance.amount -= amount
        receiver_balance.amount += amount

        self.balance_repository.save(sender_balance)
        self.balance_repository.save(receiver_balance)