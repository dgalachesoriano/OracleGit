from abc import ABC, abstractmethod
from typing import List


class IDatabaseConnector(ABC):
    @abstractmethod
    def fetch_table_data(self, table_name: str) -> List[dict]:
        """
        Recupera todas las filas de una tabla como lista de diccionarios.
        """
        pass
