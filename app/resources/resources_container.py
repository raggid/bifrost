from dependency_injector import providers, containers

from app.resources.postgres_connect import PostgresConnection


class ResourcesContainer(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    config.from_yaml('metadata.yml')

    db = providers.Singleton(PostgresConnection, config)
