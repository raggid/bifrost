from dependency_injector import containers, providers

from app.database.notas_repository import NotasRepository
from app.database.postgres_connect import PostgresConnection
from app.service.notas_service import NotasService


class Container(containers.DeclarativeContainer):
    configs = providers.Configuration('config')
    configs.from_yaml('metadata.yml')

    connection = PostgresConnection(configs()).connection
    notas_repo = providers.Singleton(NotasRepository, connection=connection)

    notas_service = providers.Singleton(NotasService, notas_repo())
