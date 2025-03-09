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