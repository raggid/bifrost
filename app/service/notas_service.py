from app.database.notas_repository import NotasRepository


class NotasService:
    repo = NotasRepository()

    def get_by_nota(self, tabela, filial, serie, nota):
        produtos = self.repo.get_notas(tabela, filial, serie, nota)
        return produtos
