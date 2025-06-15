from abc import ABC, abstractmethod
from core.domain.dto.diff_result_dto import DiffResultDTO
from typing import List


class IRollbackService(ABC):
    @abstractmethod
    def generate_rollback_sql(
        self,
        diff: DiffResultDTO,
        table_name: str,
        key_fields: List[str]
    ) -> List[str]:
        """
        A partir de un DiffResultDTO y el nombre de la tabla, genera una lista de sentencias SQL
        que revierten los cambios detectados. Se requiere que se indiquen las columnas clave.
        """
        pass
