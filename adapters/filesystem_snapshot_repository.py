import os
import json
from datetime import datetime
from typing import List
from core.domain.interfaces.snapshot_repository import ISnapshotRepository
from core.domain.models import ParamSnapshot
from adapters.serializers import snapshot_to_dict, snapshot_from_dict


class FileSystemSnapshotRepository(ISnapshotRepository):
    def __init__(self, base_path: str = "snapshots"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, snapshot: ParamSnapshot) -> None:
        folder = os.path.join(self.base_path, snapshot.table_name)
        os.makedirs(folder, exist_ok=True)

        filename = f"{snapshot.timestamp.isoformat().replace(':', '-')}.json"
        full_path = os.path.join(folder, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(snapshot_to_dict(snapshot), f, indent=2)

        print(f"[✔] Snapshot guardado en {full_path}")

    def load(self, path: str) -> ParamSnapshot:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return snapshot_from_dict(data)

    def list_snapshots(self, table_name: str) -> List[str]:
        folder = os.path.join(self.base_path, table_name)
        if not os.path.exists(folder):
            return []

        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.endswith(".json")
        ]

        return sorted(files)

    def load_latest(self, table_name: str) -> ParamSnapshot:
      snapshot_paths = self.list_snapshots(table_name)
      if not snapshot_paths:
          raise FileNotFoundError(f"No hay snapshots para la tabla '{table_name}'")

      # Cargar todos los snapshots para obtener su timestamp real
      snapshots_with_paths = [
          (self.load(path), path) for path in snapshot_paths
      ]

      # Ordenar por snapshot.timestamp (tipo datetime)
      latest_snapshot, _ = max(snapshots_with_paths, key=lambda sp: sp[0].timestamp)
      return latest_snapshot
