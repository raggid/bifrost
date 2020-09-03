from dataclasses import dataclass, field
import datetime
from typing import List


@dataclass
class NoteProduct:
    branch: int = 0
    series: str = ''
    note: int = 0
    date: datetime.date = datetime.date.today()
    note_id: str = ''
    fornecedor_emp: int = 0
    provider_code: int = 0
    provider_name: str = ''
    product_code: str = ''
    id_produto: str = ''
    product_name: str = ''
    quantity: int = 0
    unit_price: float = 0.0
    total_price: float = 0.0
    liquid_unit_price: float = 0.0
    liquid_total_price: float = 0.0


@dataclass
class Note:
    branch: int = 0
    series: str = ''
    note: int = 0
    date: datetime.date = datetime.date.today()
    note_id: str = ''
    city: str = ''
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
