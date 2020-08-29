from app.database.connections import PostgresConnection
from app.model.produto_nota import ProdutoNota


class NotasRepository:
    db = PostgresConnection().connect()

    def get_notas(self, tabela, filial, serie, nota):
        notas = []

        ps = self.get_query_by_table(tabela, filial, serie, nota)

        for record in ps.rows():
            nota = ProdutoNota(*record)
            notas.append(nota)
        return notas

    def get_query_by_table(self, tabela, filial, serie, nota):
        if tabela == 'NFA057':
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
                a.es,
                a.cliente_emp::INTEGER, 
                a.cliente_cod::INTEGER, 
                a.razao_social, 
                a.cliente_nome, 
                a.vendedor::INTEGER, 
                a.total::DOUBLE PRECISION as total_nota, 
                a.liquido::DOUBLE PRECISION as liquido_nota, 
                a.condicao, 
                a.observacao, 
                a.observacao1, 
                a.observacao2, 
                a.observacao3, 
                a.obs,
                'NFE' AS tipo,
                NULL as desconto_valor,
                NULL as desconto,
                b.fornecedor_emp::INTEGER,
                b.fornecedor_cod::INTEGER,
                b.produto, 
                b.fornecedor_cod||'___'||
                b.produto as id_produto, 
                b.quantidade::INTEGER, 
                b.unitario::DOUBLE PRECISION, 
                b.total::DOUBLE PRECISION as total_item, 
                b.liquido::DOUBLE PRECISION as liquido_item, 
                b.total_liquido::DOUBLE PRECISION
    
                from nfa057 a
                INNER JOIN nfa058 b
                ON a.filial=b.filial and a.serie=b.serie and a.nota=b.nota and a.emissao=b.nota_emissao
                where a.emissao BETWEEN to_date('01/08/2020','dd/mm/yyyy') AND current_date 
                AND a.filial = {filial} AND a.serie = '{serie}' AND a.nota = {nota} ''')
        else:
            return self.db.prepare(f'''
                select
                c.filial::INTEGER, 
                c.if as serie, 
                c.cupom::INTEGER as nota, 
                c.data as emissao,
                c.filial||'___'||
                c.if||'___'||
                c.cupom||'___'||
                c.data as id_nota,
                'S' as es,
                NULL as cliente_emp, 
                NULL as cliente_cod, 
                NULL as razao_social, 
                NULL as cliente_nome, 
                c.vendedor::INTEGER, 
                c.total::DOUBLE PRECISION as total_nota, 
                c.liquido::DOUBLE PRECISION as liquido_nota, 
                c.condicao, 
                c.obs as observacao,
                c.obs1 as observacao1, 
                NULL as observacao2, 
                NULL as observacao3, 
                NULL as obs,
                'NFCE' AS tipo,
                c.desconto_valor::DOUBLE PRECISION, 
                c.desconto::DOUBLE PRECISION, 
                d.fornecedor_emp::INTEGER, 
                d.fornecedor_cod::INTEGER, 
                d.produto,
                d.fornecedor_cod||'___'||
                d.produto as id_produto,
                d.quantidade::INTEGER, 
                d.unitario::DOUBLE PRECISION, 
                d.total::DOUBLE PRECISION as total_item, 
                d.liquido::DOUBLE PRECISION as liquido_item, 
                d.total_liquido::DOUBLE PRECISION

                from ecfa209 c
                INNER JOIN ecfa211 d on c.filial=d.filial and c.if=d.if and c.cupom=d.cupom and c.data=d.data
                where c.data BETWEEN to_date('01/08/2020','dd/mm/yyyy') AND current_date 
                AND c.filial = {filial} AND c.if = '{serie}' AND c.cupom = {nota};
                ''')
