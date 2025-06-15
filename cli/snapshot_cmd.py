import os

import click

from adapters.filesystem_snapshot_repository import FileSystemSnapshotRepository
from adapters.oracle.oracle_connector import OracleDatabaseConnector
from config.env import ORACLE_DSN, ORACLE_PASSWORD, ORACLE_USER
from core.application.snapshot_service import SnapshotService
from core.domain.models import ParamSnapshot

SNAPSHOT_DIR = "data/snapshots"


@click.group()
def snapshot():
    """Snapshot-related operations"""
    pass


@snapshot.command("create")
@click.argument("table_name")
def create_snapshot(table_name):
    """Create a snapshot for the given table"""

    # Asegurar que el directorio existe
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    # Instanciar dependencias reales para CLI
    db = OracleDatabaseConnector(
        user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN
    )
    repo = FileSystemSnapshotRepository(base_path=SNAPSHOT_DIR)
    service = SnapshotService(db_connector=db, snapshot_repository=repo)

    # Crear snapshot
    snapshot: ParamSnapshot = service.create_snapshot(table_name)
    click.echo(
        f"✅ Snapshot created at {snapshot.timestamp} with {len(snapshot.entries)} entries"
    )


@snapshot.command("list")
@click.argument("table_name")
def list_snapshots(table_name):
    """List all available snapshots for a table"""

    # Instanciar dependencias
    db = OracleDatabaseConnector(
        user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN
    )  # No se usa, pero es necesario para instanciar el servicio
    repo = FileSystemSnapshotRepository(base_path=SNAPSHOT_DIR)
    service = SnapshotService(db_connector=db, snapshot_repository=repo)

    try:
        snapshots = service.list_snapshots(table_name)
        if not snapshots:
            click.echo("⚠️  No snapshots found.")
        else:
            click.echo(f"📂 Snapshots for table '{table_name}':")
            for path in snapshots:
                click.echo(f"  └─ {path}")
    except Exception as e:
        click.echo(f"❌ Error listing snapshots: {e}")


@snapshot.command("show")
@click.argument("file_path")
def show_snapshot(file_path):
    """Show the contents of a snapshot JSON file"""

    repo = FileSystemSnapshotRepository(base_path=SNAPSHOT_DIR)

    try:
        snapshot = repo.load(file_path)
        click.echo(f"📄 Snapshot from: {snapshot.timestamp}")
        click.echo(f"📌 Table: {snapshot.table_name}")
        click.echo(f"🔢 Entries: {len(snapshot.entries)}")
        click.echo("🧾 Sample:")
        for i, entry in enumerate(snapshot.entries[:3]):
            click.echo(f"  {i + 1}. {entry.values}")
        if len(snapshot.entries) > 3:
            click.echo("  ...")
    except Exception as e:
        click.echo(f"❌ Error loading snapshot: {e}")


@snapshot.command("delete")
@click.argument("file_path")
@click.option("--force", is_flag=True, help="Delete without confirmation")
def delete_snapshot(file_path, force):
    """Delete a snapshot JSON file"""

    full_path = os.path.join(SNAPSHOT_DIR, file_path)

    if not os.path.exists(full_path):
        click.echo("❌ Snapshot not found.")
        return

    if not force:
        confirm = click.confirm(
            f"Are you sure you want to delete {file_path}?", default=False
        )
        if not confirm:
            click.echo("🛑 Deletion cancelled.")
            return

    try:
        os.remove(full_path)
        click.echo(f"🗑️ Deleted snapshot: {file_path}")
    except Exception as e:
        click.echo(f"❌ Failed to delete snapshot: {e}")
