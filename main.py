from core.application.snapshot_service import SnapshotService
from core.application.diff_service import DiffService
from adapters.mocks.mock_database_connector import MockDatabaseConnector
from adapters.filesystem_snapshot_repository import FileSystemSnapshotRepository


def main():
    db_connector = MockDatabaseConnector()
    snapshot_repo = FileSystemSnapshotRepository()
    diff_service = DiffService()

    table_name = "config_servicio"

    print("\n📸 Creando nuevo snapshot...")
    new_snapshot = SnapshotService(db_connector, snapshot_repo).create_snapshot(table_name)

    print("\n📁 Snapshots disponibles:")
    all_paths = snapshot_repo.list_snapshots(table_name)
    for p in all_paths:
        print(f" - {p}")

    if len(all_paths) < 2:
        print("\nℹ️ Aún no hay suficientes snapshots para comparar.")
        return

    # Cargar el penúltimo snapshot
    previous_snapshot_path = all_paths[-2]
    previous_snapshot = snapshot_repo.load(previous_snapshot_path)

    print(f"\n🔍 Comparando el snapshot actual con el anterior ({previous_snapshot.timestamp})...")
    diff = diff_service.compare_snapshots(previous_snapshot, new_snapshot, key_fields=["clave"])

    if diff.is_empty():
        print("✅ No hay diferencias entre snapshots.")
    else:
        print("\n➕ Añadidos:")
        for item in diff.added:
            print(item)

        print("\n➖ Eliminados:")
        for item in diff.removed:
            print(item)

        print("\n✏️ Modificados:")
        for item in diff.changed:
            print(f"- Clave: {item['key']}")
            print(f"  Antes: {item['before']}")
            print(f"  Después: {item['after']}")
            print()


if __name__ == "__main__":
    main()
