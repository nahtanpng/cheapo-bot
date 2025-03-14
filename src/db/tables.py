credential_table = '''
CREATE TABLE IF NOT EXISTS credential
(
    id         INTEGER PRIMARY KEY,
    last_daily      TEXT,
    message_counter INTEGER DEFAULT 0
);
'''

balance_table = '''
CREATE TABLE IF NOT EXISTS balance
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    amount   INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES credential(id) 
);
'''