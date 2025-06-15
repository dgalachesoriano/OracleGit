import os

import click

from adapters.filesystem_snapshot_repository import FileSystemSnapshotRepository
from core.application.diff_service import DiffService
from core.domain.dto.diff_result_dto import DiffResultDTO

SNAPSHOT_DIR = "data/snapshots"


@click.command("diff")
@click.argument("table_name")
@click.option(
    "--from", "from_file", required=True, help="Snapshot file to compare from"
)
@click.option("--to", "to_file", required=True, help="Snapshot file to compare to")
@click.option(
    "--keys", required=True, help="Comma-separated key fields to compare (e.g. id,name)"
)
def diff_snapshots(table_name, from_file, to_file, keys):
    """Compare two snapshots of a table"""

    repo = FileSystemSnapshotRepository(base_path=SNAPSHOT_DIR)
    diff_service = DiffService()

    try:
        # Cargar snapshots
        old_snapshot = repo.load(from_file)
        new_snapshot = repo.load(to_file)

        key_fields = [k.strip() for k in keys.split(",")]

        result: DiffResultDTO = diff_service.compare_snapshots(
            old=old_snapshot, new=new_snapshot, key_fields=key_fields
        )

        click.echo(f"🔍 Diff for table '{table_name}'")
        click.echo(f"➡️ From: {from_file}")
        click.echo(f"➡️ To:   {to_file}\n")

        click.echo(f"➕ Added: {len(result.added)}")
        for row in result.added[:3]:
            click.echo(f"  + {row}")
        if len(result.added) > 3:
            click.echo("  ...")

        click.echo(f"\n➖ Removed: {len(result.removed)}")
        for row in result.removed[:3]:
            click.echo(f"  - {row}")
        if len(result.removed) > 3:
            click.echo("  ...")

        click.echo(f"\n🔁 Changed: {len(result.changed)}")
        for pair in result.changed[:2]:
            click.echo(f"  ~ Key: {pair['key']}")
            click.echo(f"    Before: {pair['before']}")
            click.echo(f"    After:  {pair['after']}")
        if len(result.changed) > 2:
            click.echo("  ...")

    except Exception as e:
        click.echo(f"❌ Diff failed: {e}")
