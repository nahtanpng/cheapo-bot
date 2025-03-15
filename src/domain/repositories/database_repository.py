from abc import abstractmethod, ABC


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
