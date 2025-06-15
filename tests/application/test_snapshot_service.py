import pytest
from unittest.mock import Mock
from core.application.snapshot_service import SnapshotService
from core.domain.models import ParamSnapshot, ParamEntry
from datetime import datetime, UTC


def test_create_snapshot_calls_dependencies_correctly():
    db_connector_mock = Mock()
    fake_data = [{"clave": "timeout", "valor": "30", "activo": True}]
    db_connector_mock.fetch_table_data.return_value = fake_data

    snapshot_repo_mock = Mock()
    snapshot_repo_mock.save.side_effect = lambda s: s  # <- nombre correcto

    service = SnapshotService(
        db_connector=db_connector_mock,
        snapshot_repository=snapshot_repo_mock
    )

    snapshot = service.create_snapshot("config_servicio")

    db_connector_mock.fetch_table_data.assert_called_once_with("config_servicio")
    snapshot_repo_mock.save.assert_called_once()  # <- nombre correcto

    assert isinstance(snapshot, ParamSnapshot)
    assert snapshot.table_name == "config_servicio"
    assert snapshot.entries[0].values["clave"] == "timeout"

def test_list_snapshots_delegates_to_repository():
    snapshot_repo_mock = Mock()
    snapshot_repo_mock.list_snapshots.return_value = ["snapshots/config_servicio/20240614T102000Z.json"]

    service = SnapshotService(
        db_connector=Mock(),
        snapshot_repository=snapshot_repo_mock
    )

    result = service.list_snapshots("config_servicio")

    snapshot_repo_mock.list_snapshots.assert_called_once_with("config_servicio")
    assert isinstance(result, list)
    assert result[0].endswith(".json")

def test_load_latest_snapshot_delegates_to_repository():
    snapshot_repo_mock = Mock()
    fake_snapshot = ParamSnapshot(
        table_name="config_servicio",
        timestamp=datetime.now(UTC),
        entries=[]
    )
    snapshot_repo_mock.load_latest.return_value = fake_snapshot

    service = SnapshotService(
        db_connector=Mock(),
        snapshot_repository=snapshot_repo_mock
    )

    snapshot = service.load_latest_snapshot("config_servicio")

    snapshot_repo_mock.load_latest.assert_called_once_with("config_servicio")
    assert isinstance(snapshot, ParamSnapshot)
    assert snapshot.table_name == "config_servicio"
