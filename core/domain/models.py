from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class ParamEntry:
    values: Dict[str, any]  # una fila de la tabla de parametría


@dataclass
class ParamSnapshot:
    table_name: str
    timestamp: datetime
    entries: List[ParamEntry]
