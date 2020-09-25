from app.database.sincronizer_repository import SincronizerRepository
from app.model import KafkaMessage


from app.service.kafka_service import producer


class SincronizerService:
    def __init__(self, configs):
        self.configs = configs
        self.repo = SincronizerRepository(configs)

    def sync(self, table, recnum, operation):

        data = self.repo.get_data_by_table_and_recnum(table, recnum)
        msg = KafkaMessage(
            self.configs['filial'],
            operation,
            table,
            data)

        producer.produce(self.configs['topic_sync'], msg)

