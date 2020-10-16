import json

from pgnotify import await_pg_notifications

from app.service.sincronizer_service import SincronizerService
import logging
import sys


class PgListener:

    def __init__(self, configs):
        self.configs = configs
        logger = logging.getLogger('pg-notify-listener')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger
        self.service = SincronizerService(configs)

    def _start(self):
        for notification in await_pg_notifications(
                f'postgres://{self.configs["postgres_string"]}',
                [f'{self.configs["pg_notify_channel"]}']
        ):
            payload = json.loads(notification.payload)
            table = payload['reg_tabela']
            valores = payload['reg_dados_pk'].split('|').pop(0)
            recnum = payload['reg_recnum']
            operation = payload['reg_evento']

            if table in ('ECFA209'):
                self.service.sync(table, recnum, operation)

    def run(self):
        self._start()
