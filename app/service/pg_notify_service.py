from pgnotify import await_pg_notifications
from app.resources.configurations import Configurations
from app.service.notas_service import NotasService

configs = Configurations()


class PgNotifyNotasService:
    def __init__(self):
        self.service = NotasService()
        for notification in await_pg_notifications(
            f'postgres://{configs.postgres_string}',
            [f'{configs.configs["notas_channel"]}']
        ):
            print(notification.payload)


