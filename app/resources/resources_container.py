from dependency_injector import providers, containers

from app.resources.postgres_connect import PostgresConnection


class ResourcesContainer(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    config.from_yaml('metadata.yml')
    config.db_addr.from_env("DATA_BASE_POSTGRES")
    config.db_user.from_env("DATA_BASE_USER")
    config.db_passwd.from_env("DATA_BASE_PASSWD")
    config.db_name.from_env("DATA_BASE_NAME")

    db = providers.Singleton(PostgresConnection, config)
