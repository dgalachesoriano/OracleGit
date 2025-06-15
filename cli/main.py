import click

from cli.diff_cmd import diff_snapshots  # Importamos el comando de diff
from cli.rollback_cmd import rollback_snapshot  # Importamos el comando de rollback
from cli.snapshot_cmd import snapshot  # Importamos el grupo


# Grupo principal
@click.group()
def cli():
    """OracleGit - Version control for Oracle param tables"""
    pass


cli.add_command(snapshot)
cli.add_command(diff_snapshots)
cli.add_command(rollback_snapshot)

# Punto de entrada
if __name__ == "__main__":
    cli()
