from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def find_by_id(self, user_id: int) -> User:
        pass

    def save(self, user: User):
        pass