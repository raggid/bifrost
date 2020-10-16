from abc import ABC, abstractmethod
import postgresql


class Connection(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass


class PostgresConnection(Connection):
    def __init__(self, configs):
        super().__init__()
        self.configs = configs
        self.db = self.connect()

    def connect(self):
        db = postgresql.open(f'pq://{self.configs["postgres_string"]}')
        return db
