from dataclasses import dataclass


@dataclass
class KafkaMessage:
    source: str
    operation: str
    table: str
    data: dict
