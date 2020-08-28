from app.database.notas_repository import NotasRepository


class NotasService:
    repo = NotasRepository()

    def get_by_nota(self, filial, serie, nota):
        produtos = self.repo.get_notas(filial, serie, nota)
        return produtos