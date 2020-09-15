from app.database.connections import PostgresConnection
from app.model.produto_nota import ProdutoNota


class NotasRepository:
    db = PostgresConnection().connect()

    def get_notas(self, tabela, filial, serie, nota):
        produtos = []

        ps = self.get_query_by_table(tabela, filial, serie, nota)

        for record in ps.rows():
            produto = ProdutoNota(*record)
            produtos.append(produto)
        return produtos

    def get_query_by_table(self, tabela, filial, serie, nota):
        if tabela == 'NFA057':
            return self.db.prepare(f'''
                select 
                    a.filial||'___'||
                    a.serie||'___'||
                    a.nota||'___'|| 
                    a.emissao||'___'||
                    b.fornecedor_cod||'___'||
                    b.produto as id_nota_produto,
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
                    e.nome as condicao, 
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
                    d.nome as fornecedor,
                    b.produto, 
                    b.fornecedor_cod||'___'||
                    b.produto as id_produto,
                    b.produto_desc as nome_produto,
                    b.quantidade::INTEGER, 
                    b.unitario::DOUBLE PRECISION, 
                    b.total::DOUBLE PRECISION as total_item, 
                    b.liquido::DOUBLE PRECISION as liquido_item, 
                    b.total_liquido::DOUBLE PRECISION
                from nfa057 a
                INNER JOIN nfa058 b ON a.filial=b.filial 
                    and a.serie=b.serie and a.nota=b.nota and a.emissao=b.nota_emissao
                INNER JOIN ags022 c on a.filial = c.codigo
                INNER JOIN ags031 d ON b.fornecedor_cod = d.codigo and b.fornecedor_emp = d.empresa
                INNER JOIN ags039 e ON a.condicao = e.codigo
                where a.filial = {filial} AND a.serie = '{serie}' AND a.nota = {nota} 
                    and a.es = 'S' and a.transf_destino = 0 ''')
        elif tabela == 'ECFA209':
            return self.db.prepare(f'''
                select
                    a.filial||'___'||
                    a.if||'___'||
                    a.cupom||'___'||
                    a.filial||'___'||
                    b.fornecedor_cod||'___'||
                    b.produto as id_nota_produto,
                    a.filial::INTEGER,
                    a.if as serie, 
                    a.cupom::INTEGER as nota, 
                    a.data as emissao,
                    a.filial||'___'||
                    a.if||'___'||
                    a.cupom||'___'||
                    a.data as id_nota,
                    c.cidade,
                    'S' as es,
                    NULL as cliente_emp, 
                    NULL as cliente_cod, 
                    NULL as razao_social, 
                    a.cliente_nome as cliente_nome, 
                    a.vendedor::INTEGER, 
                    a.total::DOUBLE PRECISION as total_nota, 
                    a.liquido::DOUBLE PRECISION as liquido_nota, 
                    e.nome as condicao, 
                    a.obs as observacao,
                    a.obs1 as observacao1, 
                    NULL as observacao2, 
                    NULL as observacao3, 
                    NULL as obs,
                    'NFCE' AS tipo,
                    a.desconto_valor::DOUBLE PRECISION, 
                    a.desconto::DOUBLE PRECISION, 
                    b.fornecedor_emp::INTEGER, 
                    b.fornecedor_cod::INTEGER, 
                    d.nome as fornecedor,
                    b.produto,
                    b.fornecedor_cod||'___'||
                    b.produto as id_produto,
                    b.descri_cf as nome_produto,
                    b.quantidade::INTEGER, 
                    b.unitario::DOUBLE PRECISION, 
                    b.total::DOUBLE PRECISION as total_item, 
                    b.liquido::DOUBLE PRECISION as liquido_item, 
                    b.total_liquido::DOUBLE PRECISION                  
                from ecfa209 a
                INNER JOIN ecfa211 b on a.filial=b.filial and a.if=b.if and a.cupom=b.cupom and a.data=b.data
                INNER JOIN ags022 c on a.filial = c.codigo
                INNER JOIN ags031 d ON b.fornecedor_cod = d.codigo and b.fornecedor_emp = d.empresa
                INNER JOIN ags039 e ON a.condicao = e.codigo
                where a.filial = {filial} AND a.if = '{serie}' AND a.cupom = {nota} 
                ''')


