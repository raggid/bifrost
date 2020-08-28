from abc import ABC, abstractmethod
import postgresql

from app.resources.configurations import Configurations


class Connection(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass


class PostgresConnection(Connection):
    configs = Configurations().configs

    def __init__(self):
        super().__init__()

    def connect(self):
        db = postgresql.open(f'pq://{self.configs["db_user"]}:{self.configs["db_passwd"]}@{self.configs["db_addr"]}:5432/{self.configs["db_name"]}')
        return db
