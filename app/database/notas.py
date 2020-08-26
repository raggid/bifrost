
class Notas(object):
    def __init__(self, database):
        self._db = database.db

    def get_notas(self, filial, serie, nota):
        return self._db.all(
        f'''
        select 
        a.filial,
        a.serie,
        a.nota, 
        a.emissao,
        a.filial||'___'||
        a.serie||'___'||
        a.nota||'___'|| 
        a.emissao as id_nota,
        a.es,
        a.cliente_emp, 
        a.cliente_cod, 
        a.razao_social, 
        a.cliente_nome, 
        a.vendedor, 
        a.total as total_nota, 
        a.liquido as liquido_nota, 
        a.condicao, 
        a.observacao, 
        a.observacao1, 
        a.observacao2, 
        a.observacao3, 
        a.obs,
        'NFE' AS tipo,
        NULL as desconto_valor,
        NULL as desconto,
        b.fornecedor_emp,
        b.fornecedor_cod,
        b.produto, 
        b.fornecedor_cod||'___'||
        b.produto as id_produto, 
        b.quantidade, 
        b.unitario, 
        b.total as total_item, 
        b.liquido as liquido_item, 
        b.total_liquido
        
        from nfa057 a
        INNER JOIN nfa058 b
        ON a.filial=b.filial and a.serie=b.serie and a.nota=b.nota and a.emissao=b.nota_emissao
        where a.emissao BETWEEN to_date('01/08/2020','dd/mm/yyyy') AND current_date 
        AND a.filial = {filial} AND a.serie = '{serie}' AND a.nota = {nota} 
        
        UNION all
        
        select
        c.filial, 
        c.if as serie, 
        c.cupom as nota, 
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
        c.vendedor, 
        c.total as total_nota, 
        c.liquido as liquido_nota, 
        c.condicao, 
        c.obs as observacao,
        c.obs1 as observacao1, 
        NULL as observacao2, 
        NULL as observacao3, 
        NULL as obs,
        'NFCE' AS tipo,
        c.desconto_valor, 
        c.desconto, 
        d.fornecedor_emp, 
        d.fornecedor_cod, 
        d.produto,
        d.fornecedor_cod||'___'||
        d.produto as id_produto,
        d.quantidade, 
        d.unitario, 
        d.total as total_item, 
        d.liquido as liquido_item, 
        d.total_liquido
        
        from ecfa209 c
        INNER JOIN ecfa211 d on c.filial=d.filial and c.if=d.if and c.cupom=d.cupom and c.data=d.data
        where c.data BETWEEN to_date('01/08/2020','dd/mm/yyyy') AND current_date 
        AND c.filial = {filial} AND c.if = '{serie}' AND c.cupom = {nota};
        ''')
