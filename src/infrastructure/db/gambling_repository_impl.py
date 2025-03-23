from src.domain.repositories.gambling_repository import GamblingRepository


class GamblingRepositoryImpl(GamblingRepository):
    def __init__(self, connection):
        self.conn = connection

    def flip_reward(self, user_id: int, value: int, is_winner: bool):
        c = self.conn.cursor()
        c.execute('INSERT OR IGNORE INTO credential (id) VALUES (?)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (amount, user_id) VALUES (?, ?)', (0, user_id,))

        if is_winner:
            c.execute('UPDATE balance SET amount = amount + ? WHERE user_id = ?', (value, user_id))
        else:
            c.execute('UPDATE balance SET amount = amount - ? WHERE user_id = ?', (value, user_id))
        self.conn.commit()