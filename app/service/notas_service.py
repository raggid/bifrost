from app.database.notas_repository import NotasRepository
from app.resources.configurations import Configurations


from app.service.kafka_service import producer


class NotasService:
    configs = Configurations()
    topic_notas = configs.configs['topic_notas']
    repo = NotasRepository()

    def process(self, tabela, valores):
        products = self.get_by_nota(tabela, int(valores[1]), valores[2], int(valores[3]))
        for product in products:
            producer.produce(self.topic_notas, product)

    def get_by_nota(self, tabela, filial, serie, nota):
        produtos = self.repo.get_notas(tabela, filial, serie, nota)
        return produtos
