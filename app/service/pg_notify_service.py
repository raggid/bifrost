from pgnotify import await_pg_notifications
from app.resources.configurations import Configurations
from app.service.notas_service import NotasService
import threading
from threading import Event
import logging
import sys
import signal

configs = Configurations()
service = NotasService()


class NotifListener:

    def __init__(self, interrupt_event):
        self.interrupt_event = interrupt_event
        logger = logging.getLogger('pg-notify-listener')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def signal_term_handler(self, signal, frame):
        self.logger.info("stopping listener")
        # self.consumer.close()
        sys.exit(0)

    def interrupted_process(self, *args):
        self.logger.info("stopping listener")
        # self.consumer.close()
        sys.exit(0)

    def _start(self):
        for notification in await_pg_notifications(
                f'postgres://{configs.postgres_string}',
                [f'{configs.configs["pg_notify_channel"]}']
        ):
            payload = notification.payload
            tabela = payload['reg_tabela']
            colunas = payload['reg_cols_pk'].split('|')
            valores = payload['reg_dados_pk'].split('|')

            service.get_by_nota(tabela, valores[0], valores[1], valores[2])

    def _run(self):
        self.logger.info(" * The application is listening")
        t = threading.Thread(target=self._start)
        t.start()

    def run(self):
        self._run()


INTERRUPT_EVENT = Event()
listener = NotifListener(INTERRUPT_EVENT)



