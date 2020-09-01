import json
import logging
import sys

from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.errors import KafkaError
import jsonpickle

from app.resources.configurations import Configurations

configs = Configurations()

filial = configs.configs['filial']
kafka_broker = f"{configs.configs['kafka_server']}:9092"


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
            # self.logger.exception(KafkaError)
            pass
        self.logger.info(f"Sent new data to topic {record_metadata.topic} on offset {record_metadata.offset}")
        return data


producer = PgKafkaProducer(bootstrap_servers=",".join([kafka_broker]),
                              client_id=f"filial-{filial}"
                              # max_request_size=10000000
                              )
