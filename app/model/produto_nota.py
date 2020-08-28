from dataclasses import dataclass
import datetime

@dataclass
class ProdutoNota:
    filial: int = 0
    serie: str = ''
    nota: int = 0
    emissao: datetime.date = datetime.date.today()
    id_nota: str = ''
    es: str = ''
    cliente_emp: int = 0
    cliente_cod: int = 0
    razao_social: str = ''
    cliente_nome: str = ''
    vendedor: int = 0
    total_nota: float = 0.0
    liquido_nota: float = 0.0
    condicao: str = ''
    observacao: str = ''
    observacao1: str = ''
    observacao2: str = ''
    observacao3: str = ''
    obs: str = ''
    tipo: str = ''
    desconto_valor: float = 0.0
    desconto: float = 0
    fornecedor_emp: int = 0
    fornecedor_cod: int = 0
    produto: str = ''
    id_produto: str = ''
    quantidade: int = 0
    unitario: float = 0.0
    total_item: float = 0.0
    liquido_item: float = 0.0
    total_liquido: float = 0.0