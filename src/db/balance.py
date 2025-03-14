import sqlite3


def get_balance(user_id):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0


def update_balance(user_id, amount):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
    c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()


def verify_balance(user_id, value):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
    c.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False, 0

    balance = result[0]
    if balance < value:
        return False, balance
    else:
        return True, balance


def set_last_daily(user_id, date):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('UPDATE users SET last_daily = ? WHERE user_id = ?', (date, user_id))
    conn.commit()
    conn.close()


def get_last_daily(user_id):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT last_daily FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def add_reward_every_ten_message(user_id):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()

    # Create the user, if it doesn't exist
    c.execute('INSERT OR IGNORE INTO users (user_id, balance, message_counter) VALUES (?, 0, 0)', (user_id,))

    # Increment the counter
    c.execute('UPDATE users SET message_counter = message_counter + 1 WHERE user_id = ?', (user_id,))

    # Check the counter value
    c.execute('SELECT message_counter FROM users WHERE user_id = ?', (user_id,))
    counter = c.fetchone()[0]

    if counter == 10:
        c.execute('UPDATE users SET balance = balance + 1, message_counter = 0 WHERE user_id = ?', (user_id,))

    conn.commit()
    conn.close()


def pay(sender_id: int, receiver_id: int, value: int):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)', (sender_id, 0,))
    c.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)', (receiver_id, 0,))

    c.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (value, sender_id,))
    c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (value, receiver_id,))

    conn.commit()
    conn.close()
