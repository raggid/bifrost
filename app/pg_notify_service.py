import json

from pgnotify import await_pg_notifications
from app.resources.configurations import Configurations
from app.service.kafka_service import PgKafkaProducer
from app.service.notas_service import NotasService
import logging
import sys

configs = Configurations()
service = NotasService()
producer = PgKafkaProducer()

topic_notas = configs.configs['topic_notas']

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
            colunas = payload['reg_cols_pk'].split('|')
            valores = payload['reg_dados_pk'].split('|')

            self.logger.info(f'{tabela} updated')
            self.logger.info('Sending to kafka')
            produtos = service.get_by_nota(tabela, int(valores[1]), valores[2], int(valores[3]))

            for value in produtos:
                producer.produce(topic_notas, value)

            print(produtos)

    def run(self):
        self._start()
