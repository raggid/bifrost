from abc import ABC, abstractmethod
import postgresql

from app.resources.configurations import Configurations

configs = Configurations()


class Connection(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass


class PostgresConnection(Connection):
    def __init__(self):
        super().__init__()

    def connect(self):
        db = postgresql.open(f'pq://{configs.postgres_string}')
        return db
