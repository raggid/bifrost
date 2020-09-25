from app.database.connections import PostgresConnection


class SincronizerRepository:

    def __init__(self, config):
        self.db = PostgresConnection(config).connect()

    def get_data_by_table_and_recnum(self, table, recnum):
        ps = self.db.prepare(f"SELECT * FROM {table} WHERE RECNUM = $1")

        record = ps.first(recnum)
        columns = record.column_names
        values = [*record]

        data = dict(zip(columns, values))

        return data
