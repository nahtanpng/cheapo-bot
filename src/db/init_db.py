from abc import ABC, abstractmethod
from sqlite3 import Connection, connect

from src.db.tables import balance_table, credential_table

class DatabaseInterface(ABC):
    @abstractmethod
    def init_db(self) -> None:
        pass

    @abstractmethod
    def close_conn(self) -> None:
        pass

    @abstractmethod
    def init_tables(self) -> None:
        pass


class Database(DatabaseInterface):
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
