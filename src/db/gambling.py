import sqlite3


def flip_reward(user_id: int, value: int, is_winner: bool):
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
    if is_winner:
        c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (value, user_id))
    else:
        c.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (value, user_id))
    conn.commit()
    conn.close()
