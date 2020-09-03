from app.database.notas_repository import NotesRepository
from app.resources.configurations import Configurations

from app.service.kafka_service import producer


class NotasService:
    configs = Configurations()
    notes_topic = configs.configs['notes_topic']
    products_topic = configs.configs['products_topic']
    repo = NotesRepository()

    def process(self, table, values):
        note = self.repo.get_note(table, int(values[1]), values[2], int(values[3]))

        if note is not None:
            products = self.repo.get_products(table, note)

            producer.produce(self.notes_topic, note)
            for product in products:
                producer.produce(self.products_topic, product)
