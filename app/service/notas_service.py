from app.database.notas_repository import NotasRepository
from app.resources.configurations import Configurations


class NotasService:
    configs = Configurations()
    topic_notas = configs.configs['topic_notas']
    repo = NotasRepository()

    def get_data(self, tabela, valores):
        return self.topic_notas, self.get_by_nota(tabela, int(valores[1]), valores[2], int(valores[3]))

    def get_by_nota(self, tabela, filial, serie, nota):
        produtos = self.repo.get_notas(tabela, filial, serie, nota)
        return produtos
