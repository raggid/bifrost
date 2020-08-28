from envyaml import EnvYAML


class Configurations:
    def __init__(self):
        self.configs = EnvYAML('metadata.yaml')
