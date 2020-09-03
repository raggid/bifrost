import json

from pgnotify import await_pg_notifications
from app.resources.configurations import Configurations
from app.service.notas_service import NotasService
import logging
import sys

configs = Configurations()
service = NotasService()


class PgListener:

    def __init__(self):
        logger = logging.getLogger('pg-notify-listener')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def _start(self):
        for notification in await_pg_notifications(
                f'postgres://{configs.postgres_string}',
                [f'{configs.configs["pg_notify_channel"]}']
        ):
            payload = json.loads(notification.payload)
            tabela = payload['reg_tabela']
            valores = payload['reg_dados_pk'].split('|')

            if tabela == 'NFA057':
                service.process(tabela, valores)

    def run(self):
        self._start()
