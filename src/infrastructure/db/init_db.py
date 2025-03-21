from sqlite3 import Connection, connect

from src.domain.repositories.database_repository import DatabaseRepository
from src.infrastructure.db.tables import balance_table, credential_table


class Database(DatabaseRepository):
    conn: Connection

    def init_db(self):
        self.conn = connect('economy.db')
        self.init_tables()
        self.conn.commit()

    def close_conn(self):
        self.conn.close()

    def init_tables(self):
        self.conn.executescript(
            credential_table +
            balance_table,
        )
