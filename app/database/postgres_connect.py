from postgres import Postgres


class PostgresConnection:

    def __init__(self, config):
        self._config = config
        self.connection = self.connect(self._config)

    def connect(self, config):
        connection = Postgres(f'host={config["db_addr"]} dbname={config["db_name"]} user={config["db_user"]} password={config["db_passwd"]} ')
        return connection

