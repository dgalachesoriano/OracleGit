import pytest
from core.application.diff_service import DiffService
from core.domain.models import ParamSnapshot, ParamEntry
from datetime import datetime


def test_diff_service_detects_added_removed_and_changed(build_snapshot):
    diff_service = DiffService()

    snapshot_old = build_snapshot([
        {"clave": "timeout", "valor": "30", "activo": True},
        {"clave": "modo", "valor": "prod", "activo": True},
    ])

    snapshot_new = build_snapshot([
        {"clave": "timeout", "valor": "45", "activo": True},
        {"clave": "nuevo", "valor": "x", "activo": False},
    ])

    result = diff_service.compare_snapshots(snapshot_old, snapshot_new, key_fields=["clave"])

    assert len(result.added) == 1
    assert len(result.removed) == 1
    assert len(result.changed) == 1

def test_diff_service_with_composite_keys(build_snapshot):
    diff_service = DiffService()

    snapshot_old = build_snapshot([
        {"tipo": "pais", "codigo": "IT", "nombre": "Italia", "activo": True},
        {"tipo": "pais", "codigo": "PT", "nombre": "Portugal", "activo": True},
    ])

    snapshot_new = build_snapshot([
        {"tipo": "pais", "codigo": "IT", "nombre": "Italia (nuevo)", "activo": False},  # modificado
        {"tipo": "pais", "codigo": "ES", "nombre": "España", "activo": True},           # añadido
    ])

    result = diff_service.compare_snapshots(snapshot_old, snapshot_new, key_fields=["tipo", "codigo"])

    assert len(result.added) == 1
    assert result.added[0]["codigo"] == "ES"

    assert len(result.removed) == 1
    assert result.removed[0]["codigo"] == "PT"

    assert len(result.changed) == 1
    assert result.changed[0]["key"] == ("pais", "IT")

def test_diff_service_no_changes(build_snapshot):
    entries = [
        {"clave": "timeout", "valor": "30", "activo": True},
        {"clave": "modo", "valor": "prod", "activo": True},
    ]

    snapshot_old = build_snapshot(entries)
    snapshot_new = build_snapshot(entries)

    result = DiffService().compare_snapshots(snapshot_old, snapshot_new, key_fields=["clave"])

    assert result.is_empty()
    assert result.added == []
    assert result.removed == []
    assert result.changed == []

def test_diff_service_ignores_partial_key_match(build_snapshot):
    snapshot_old = build_snapshot([
        {"tipo": "X", "codigo": "1", "nombre": "Original"},
    ])
    snapshot_new = build_snapshot([
        {"tipo": "Y", "codigo": "1", "nombre": "Original"},
    ])

    result = DiffService().compare_snapshots(snapshot_old, snapshot_new, key_fields=["tipo", "codigo"])

    assert len(result.added) == 1
    assert len(result.removed) == 1
    assert result.changed == []

def test_diff_service_with_none_values(build_snapshot):
    snapshot_old = build_snapshot([
        {"clave": "modo", "valor": None},
    ])
    snapshot_new = build_snapshot([
        {"clave": "modo", "valor": "activo"},
    ])

    result = DiffService().compare_snapshots(snapshot_old, snapshot_new, key_fields=["clave"])

    assert len(result.changed) == 1
    assert result.changed[0]["before"]["valor"] is None
    assert result.changed[0]["after"]["valor"] == "activo"
