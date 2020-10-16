import json
import logging
import sys
import threading

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
import jsonpickle

from app.resources.configurations import Configurations

configs = Configurations()

filial = configs.configs['filial']
kafka_broker = f"{configs.configs['kafka_server']}:6667"


class FlaskKafka:
    def __init__(self, interrupt_event, **kw):
        self.consumer = KafkaConsumer(**kw)
        self.handlers = {}
        self.interrupt_event = interrupt_event
        logger = logging.getLogger('flask-kafka-consumer')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def _add_handler(self, topic, handler):
        if self.handlers.get(topic) is None:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def handle(self, topic):
        def decorator(f):
            self._add_handler(topic, f)
            return f

        return decorator

    def _run_handlers(self, msg):
        try:
            handlers = self.handlers[msg.topic]
            for handler in handlers:
                handler(msg)
            self.consumer.commit()
        except Exception as e:
            self.logger.critical(str(e), exc_info=1)
            self.consumer.seek(TopicPartition(msg.topic, 0), msg.offset)
            # sys.exit("Exited due to exception")

    def signal_term_handler(self, signal, frame):
        self.logger.info("closing consumer")
        self.consumer.close()
        sys.exit(0)

    def _start(self):
        partitions = []
        for key in self.handlers.keys():
            partitions.append(TopicPartition(key, 0))
        self.consumer.assign(partitions)
        self.logger.info("starting consumer...registered signterm")

        for msg in self.consumer:
            msg_source = json.loads(msg.value.decode("utf-8"))['source']
            if msg_source != filial:
                msg_content = json.loads(msg.value.decode("utf-8"))['content']
                self.logger.info("TOPIC: {}, PAYLOAD: {}".format(msg.topic, msg_content['id']))
                self._run_handlers(msg)
            # stop the consumer
            if self.interrupt_event.is_set():
                self.interrupted_process()
                self.interrupt_event.clear()
            # else:
            #     self.consumer.commit()

    def interrupted_process(self, *args):
        self.logger.info("closing consumer")
        self.consumer.close()
        sys.exit(0)

    def _run(self):
        self.logger.info(" * The flask Kafka application is consuming")
        t = threading.Thread(target=self._start)
        t.start()

    # run the consumer application
    def run(self):
        self._run()


class PgKafkaProducer:
    def __init__(self, **kw):
        self.producer = KafkaProducer(**kw)
        logger = logging.getLogger('flask-kafka-producer')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def produce(self, topic, data):
        self.logger.info(f"Sending new data to {topic}")
        payload = jsonpickle.encode(data, make_refs=False, unpicklable=False).encode('utf-8')
        future = self.producer.send(topic, payload)
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            self.produce(topic, data)
            pass
        self.logger.info(f"Sent new data to topic {record_metadata.topic} on offset {record_metadata.offset}")
        return data


INTERRUPT_EVENT = threading.Event()

consumer = FlaskKafka(INTERRUPT_EVENT,
                      bootstrap_servers=",".join([kafka_broker]),
                      group_id=f"filial-{filial}",
                      max_partition_fetch_bytes=10000000
                      )

producer = PgKafkaProducer(bootstrap_servers=",".join([kafka_broker]),
                           client_id=f"filial-{filial}",
                           max_request_size=10000000
                           )
