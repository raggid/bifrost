from app.database.connections import PostgresConnection
from app.model.produto_nota import NoteProduct, Note


class NotesRepository:
    db = PostgresConnection().connect()

    def get_note(self, table, branch, series, note):

        ps = self.get_query_by_table(table, branch, series, note)
        invoice = Note(*ps()[0])

        # if invoice is not None:
        #     ps = self.get_products_by_note(table, branch, series, note)
        #     for record in ps.rows():
        #         product = NoteProduct(*record)
        #         invoice.products.append(product)
        return invoice

    def get_query_by_table(self, table, branch, series, note):
        if table == 'NFA057':
            return self.db.prepare(f'''
                select 
                    a.filial::INTEGER,
                    a.serie,
                    a.nota::INTEGER, 
                    a.emissao,
                    a.filial||'___'||
                    a.serie||'___'||
                    a.nota||'___'|| 
                    a.emissao as id_nota,
                    c.cidade,
                    a.es,
                    a.cliente_emp::INTEGER, 
                    a.cliente_cod::INTEGER, 
                    a.razao_social, 
                    a.cliente_nome, 
                    a.vendedor::INTEGER, 
                    a.total::DOUBLE PRECISION as total_nota, 
                    a.liquido::DOUBLE PRECISION as liquido_nota, 
                    d.nome as condicao,
                    a.observacao, 
                    a.observacao1, 
                    a.observacao2, 
                    a.observacao3, 
                    a.obs,
                    'NFE' AS tipo,
                    NULL as desconto_valor,
                    NULL as desconto
                from nfa057 a
                INNER JOIN ags022 c on a.filial = c.codigo
                INNER JOIN ags039 d on a.condicao = d.codigo
                where a.filial = {branch} AND a.serie = '{series}' AND a.nota = {note} ''')
        # else:
        #     return self.db.prepare(f'''
        #         select
        #         c.filial::INTEGER,
        #         c.if as serie,
        #         c.cupom::INTEGER as nota,
        #         c.data as emissao,
        #         c.filial||'___'||
        #         c.if||'___'||
        #         c.cupom||'___'||
        #         c.data as id_nota,
        #         'S' as es,
        #         NULL as cliente_emp,
        #         NULL as cliente_cod,
        #         NULL as razao_social,
        #         NULL as cliente_nome,
        #         c.vendedor::INTEGER,
        #         c.total::DOUBLE PRECISION as total_nota,
        #         c.liquido::DOUBLE PRECISION as liquido_nota,
        #         c.condicao,
        #         c.obs as observacao,
        #         c.obs1 as observacao1,
        #         NULL as observacao2,
        #         NULL as observacao3,
        #         NULL as obs,
        #         'NFCE' AS tipo,
        #         c.desconto_valor::DOUBLE PRECISION,
        #         c.desconto::DOUBLE PRECISION,
        #         d.fornecedor_emp::INTEGER,
        #         d.fornecedor_cod::INTEGER,
        #         d.produto,
        #         d.fornecedor_cod||'___'||
        #         d.produto as id_produto,
        #         d.quantidade::INTEGER,
        #         d.unitario::DOUBLE PRECISION,
        #         d.total::DOUBLE PRECISION as total_item,
        #         d.liquido::DOUBLE PRECISION as liquido_item,
        #         d.total_liquido::DOUBLE PRECISION
        #
        #         from ecfa209 c
        #         INNER JOIN ecfa211 d on c.filial=d.filial and c.if=d.if and c.cupom=d.cupom and c.data=d.data
        #         where c.filial = {filial} AND c.if = '{serie}' AND c.cupom = {nota};
        #         ''')

    def get_products(self, table, invoice):
        ps = self.get_products_by_note(table, invoice.branch, invoice.series, invoice.note)
        products = [NoteProduct(*row) for row in ps.rows()]
        return products

    def get_products_by_note(self, table, branch, series, note):
        if table == 'NFA057':
            return self.db.prepare(f'''
                select
                    b.filial::INTEGER,
                    b.serie,
                    b.nota::INTEGER,
                    b.nota_emissao as emissao,
                    b.filial||'___'||
                    b.serie||'___'||
                    b.nota||'___'|| 
                    b.nota_emissao as id_nota,
                    b.fornecedor_emp::INTEGER,
                    b.fornecedor_cod::INTEGER,
                    e.nome as fornecedor,
                    b.produto, 
                    b.fornecedor_cod||'___'||
                    b.produto as id_produto,
                    b.produto_desc as nome_produto,
                    b.quantidade::INTEGER, 
                    b.unitario::DOUBLE PRECISION, 
                    b.total::DOUBLE PRECISION as total_item, 
                    b.liquido::DOUBLE PRECISION as liquido_item, 
                    b.total_liquido::DOUBLE PRECISION    
                from nfa058 b                
                INNER JOIN ags031 e on b.fornecedor_cod = e.codigo and b.fornecedor_emp = e.empresa
                where b.filial = {branch} AND b.serie = '{series}' AND b.nota = {note} ''')
