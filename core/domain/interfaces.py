from abc import ABC, abstractmethod
from .models import ParamSnapshot

class ISnapshotRepository(ABC):
    @abstractmethod
    def save(self, snapshot: ParamSnapshot) -> None:
        pass

    @abstractmethod
    def load(self, path: str) -> ParamSnapshot:
        pass

class IDatabaseConnector(ABC):
    @abstractmethod
    def fetch_table_data(self, table_name: str) -> list[dict]:
        pass
