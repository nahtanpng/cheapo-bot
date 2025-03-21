from src.domain.entities.balance import Balance
from src.domain.repositories.balance_repository import BalanceRepository


class BalanceRepositoryImpl(BalanceRepository):
    def __init__(self, connection):
        self.conn = connection

    def find_by_user_id(self, user_id: int) -> Balance:
        c = self.conn.cursor()
        c.execute('INSERT OR IGNORE INTO credential (id) VALUES (?)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (amount, user_id) VALUES (?, ?)', (0, user_id,))

        self.conn.commit()

        c.execute('SELECT amount FROM balance WHERE user_id = ?', (user_id,))
        result = c.fetchone()

        if result:
            balance_id, user_id, amount = result
            return Balance(balance_id, user_id, amount)
        else:
            return Balance(0, user_id, 0)

    def get_amount(self, user_id: int) -> int:
        c = self.conn.cursor()
        c.execute('INSERT OR IGNORE INTO credential (id) VALUES (?)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (amount, user_id) VALUES (?, ?)', (0, user_id,))

        self.conn.commit()

        c.execute('SELECT amount FROM balance WHERE user_id = ?', (user_id,))
        result = c.fetchone()

        return result[0] if result else 0

    def save(self, balance: Balance):
        c = self.conn.cursor()

        c.execute('SELECT id FROM balance WHERE user_id = ?', (balance.user_id,))
        result = c.fetchone()

        if result:
            c.execute('''
                UPDATE balance
                SET amount = ?
                WHERE user_id = ?
            ''', (balance.amount, balance.user_id))
        else:
            c.execute('''
                INSERT INTO balance (user_id, amount)
                VALUES (?, ?)
            ''', (balance.user_id, balance.amount))

        self.conn.commit()
