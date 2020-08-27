class NotasService(object):
    def __init__(self, database):
        self._db = database

    def get_by_nota(self, filial: int, serie: str, nota: int):
        transactions = self._db.get_transactions_by_nota(filial, serie, nota)
        return transactions
