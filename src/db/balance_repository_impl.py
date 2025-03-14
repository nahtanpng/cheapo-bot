import sqlite3

from src.db.init_db import Database


class BalanceRepository:
    def __init__(self, db: Database):
        self.db = db
        self.conn = db.conn

    def get_balance(self, user_id):
        conn = self.conn
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO credential (id) VALUES (?)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (amount, user_id) VALUES (?, ?)', (0, user_id,))

        conn.commit()

        c.execute('SELECT amount FROM balance WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0

    def update_balance(self, user_id, amount):
        conn = self.conn
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO credential (id) VALUES (?)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (amount, user_id) VALUES (?, ?)', (0, user_id,))

        c.execute('UPDATE balance SET amount = amount + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        conn.close()

    def verify_balance(self, user_id, value):
        conn = self.conn
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO user (user_id) VALUES (?)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (user_id) VALUES (?)', (user_id,))

        c.execute('SELECT amount FROM balance WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()

        if result is None:
            return False, 0

        balance = result[0]
        if balance < value:
            return False, balance
        else:
            return True, balance

    def set_last_daily(self, user_id, date):
        conn = self.conn
        c = conn.cursor()
        c.execute('UPDATE credential SET last_daily = ? WHERE id = ?', (date, user_id))
        conn.commit()
        conn.close()

    def get_last_daily(self, user_id):
        conn = self.conn
        c = conn.cursor()
        c.execute('SELECT last_daily FROM credential WHERE id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def add_reward_every_ten_message(self, user_id):
        conn = self.conn
        c = conn.cursor()

        # Create the user, if it doesn't exist
        c.execute('INSERT OR IGNORE INTO credential (id, message_counter) VALUES (?, 0)', (user_id,))
        c.execute('INSERT OR IGNORE INTO balance (amount, user_id) VALUES (?, ?)', (0, user_id,))

        # Increment the counter
        c.execute('UPDATE credential SET message_counter = message_counter + 1 WHERE id = ?', (user_id,))

        # Check the counter value
        c.execute('SELECT message_counter FROM credential WHERE id = ?', (user_id,))
        counter = c.fetchone()[0]

        if counter == 10:
            c.execute('UPDATE balance SET amount = amount + 1 WHERE user_id = ?', (user_id,))
            c.execute('UPDATE credential SET message_counter = 0  WHERE id = ?', (user_id,))

        conn.commit()
        conn.close()

    def pay(self, sender_id: int, receiver_id: int, value: int):
        conn = self.conn
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO credential (user_id) VALUES (?)', (sender_id,))
        c.execute('INSERT OR IGNORE INTO credential (user_id) VALUES (?)', (receiver_id,))

        c.execute('UPDATE balance SET amount = amount - ? WHERE user_id = ?', (value, sender_id,))
        c.execute('UPDATE balance SET amount = amount + ? WHERE user_id = ?', (value, receiver_id,))

        conn.commit()
        conn.close()
