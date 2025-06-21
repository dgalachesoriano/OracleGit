from datetime import UTC, datetime
from typing import List

from core.domain.interfaces.database_connector import IDatabaseConnector
from core.domain.interfaces.snapshot_repository import ISnapshotRepository
from core.domain.models import ParamEntry, ParamSnapshot


class SnapshotService:
    def __init__(
        self, db_connector: IDatabaseConnector, snapshot_repository: ISnapshotRepository
    ):
        self.db_connector = db_connector
        self.snapshot_repository = snapshot_repository

    def create_snapshot(self, table_name: str) -> ParamSnapshot:
        """
        Extrae los datos de la tabla de parametría y crea un snapshot con timestamp.
        Luego lo guarda usando el repositorio.
        """
        raw_rows = self.db_connector.fetch_table_data(table_name)
        entries = [ParamEntry(values=row) for row in raw_rows]

        snapshot = ParamSnapshot(
            table_name=table_name, timestamp=datetime.now(UTC), entries=entries
        )

        self.snapshot_repository.save(snapshot)
        return snapshot

    def list_snapshots(self, table_name: str) -> List[str]:
        """
        Devuelve las rutas a todos los snapshots existentes para una tabla.
        """
        return self.snapshot_repository.list_snapshots(table_name)

    def load_latest_snapshot(self, table_name: str) -> ParamSnapshot:
        """
        Devuelve el último snapshot guardado de una tabla.
        """
        return self.snapshot_repository.load_latest(table_name)
