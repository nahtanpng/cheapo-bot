from src.domain.services.gambling_service import GamblingService


class GamblingUseCase:
    def __init__(self, gambling_service: GamblingService):
        self.gambling_service = gambling_service

    def flip(self, user_id: int, side: str, amount: int):
        return self.gambling_service.flip(user_id, side, amount)
