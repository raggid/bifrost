from dataclasses import dataclass
import datetime

@dataclass
class ProdutoNota:
    branch: int = 0
    series: str = ''
    note: int = 0
    date: datetime.date = datetime.date.today()
    id_nota: str = ''
    es: str = ''
    client_company: int = 0
    client_code: int = 0
    corporate_name: str = ''
    client_name: str = ''
    salesman: int = 0
    total_order: float = 0.0
    liquid_order: float = 0.0
    condition_payment: str = ''
    observacao: str = ''
    observacao1: str = ''
    observacao2: str = ''
    observacao3: str = ''
    obs: str = ''
    tipo: str = ''
    desconto_valor: float = 0.0
    discount: float = 0
    fornecedor_emp: int = 0
    provider_code: int = 0
    product_code: str = ''
    id_produto: str = ''
    quantity: int = 0
    unit_price: float = 0.0
    total_price: float = 0.0
    liquid_unit_price: float = 0.0
    liquid_total_price: float = 0.0