from core.domain.interfaces.snapshot_repository import ISnapshotRepository
from core.domain.models import ParamSnapshot


class MockSnapshotRepository(ISnapshotRepository):
    def __init__(self):
        # Usamos un diccionario en memoria para simular el almacenamiento
        self._storage = {}

    def save(self, snapshot: ParamSnapshot) -> None:
        # Generamos una clave única: tabla + timestamp
        key = f"{snapshot.table_name}:{snapshot.timestamp.isoformat()}"
        self._storage[key] = snapshot
        print(f"[MOCK] Snapshot guardado en memoria: {key}")

    def load(self, path: str) -> ParamSnapshot:
        # En este mock, el 'path' es la clave simulada
        snapshot = self._storage.get(path)
        if not snapshot:
            raise FileNotFoundError(
                f"[MOCK] Snapshot no encontrado para la clave '{path}'"
            )
        return snapshot
