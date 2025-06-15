from abc import ABC, abstractmethod
from typing import List
from core.domain.models import ParamSnapshot


class ISnapshotRepository(ABC):
    @abstractmethod
    def save(self, snapshot: ParamSnapshot) -> None:
        pass

    @abstractmethod
    def load(self, path: str) -> ParamSnapshot:
        pass

    @abstractmethod
    def list_snapshots(self, table_name: str) -> List[str]:
        """Devuelve una lista de rutas a los snapshots de una tabla."""
        pass

    @abstractmethod
    def load_latest(self, table_name: str) -> ParamSnapshot:
        """Carga el último snapshot (por timestamp) de una tabla."""
        pass
