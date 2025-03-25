from src.domain.services.payment_service import PaymentService


class TransferCoinsUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self, sender_id: int, receiver_id: int, amount: int):
        self.payment_service.transfer(sender_id, receiver_id, amount)