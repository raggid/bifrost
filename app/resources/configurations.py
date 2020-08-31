from envyaml import EnvYAML


class Configurations:
    def __init__(self):
        self.configs = EnvYAML('metadata.yaml')
        self.postgres_string = f'{self.configs["db_user"]}:{self.configs["db_passwd"]}@{self.configs["db_addr"]}:5432/{self.configs["db_name"]}'
