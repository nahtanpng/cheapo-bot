from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, connection):
        self.conn = connection

    def find_by_id(self, user_id: int) -> User:
        pass

    def get_last_daily(self, user_id: int) -> str:
        conn = self.conn
        c = conn.cursor()
        c.execute('SELECT last_daily FROM credential WHERE id = ?', (user_id,))
        result = c.fetchone()
        return result[0] if result else None

    def set_last_daily(self, user_id: int, date: str):
        c = self.conn.cursor()
        c.execute('UPDATE credential SET last_daily = ? WHERE id = ?', (date, user_id))
        self.conn.commit()

    def save(self, user: User):
        pass