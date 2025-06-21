import pytest

from core.application.rollback_service import RollbackService
from core.domain.dto.diff_result_dto import DiffResultDTO


def test_rollback_sql_generation(diff_result_example):
    rollback_service = RollbackService()

    sql_statements = rollback_service.generate_rollback_sql(
        diff=diff_result_example, table_name="config_servicio", key_fields=["clave"]
    )

    assert len(sql_statements) == 3

    delete_sql = sql_statements[0]
    insert_sql = sql_statements[1]
    update_sql = sql_statements[2]

    # Verifica DELETE
    assert "DELETE FROM config_servicio" in delete_sql
    assert "clave = 'nuevo'" in delete_sql

    # Verifica INSERT
    assert "INSERT INTO config_servicio" in insert_sql
    assert "modo" in insert_sql
    assert "'prod'" in insert_sql

    # Verifica UPDATE
    assert "UPDATE config_servicio" in update_sql
    assert "valor = '30'" in update_sql
    assert "clave = 'timeout'" in update_sql


def test_rollback_sql_with_composite_keys(diff_compuesto_example):
    rollback_service = RollbackService()

    sql_statements = rollback_service.generate_rollback_sql(
        diff=diff_compuesto_example,
        table_name="param_paises",
        key_fields=["tipo", "codigo"],
    )

    assert len(sql_statements) == 3

    delete_sql = sql_statements[0]
    insert_sql = sql_statements[1]
    update_sql = sql_statements[2]

    # DELETE con clave compuesta
    assert "DELETE FROM param_paises" in delete_sql
    assert "tipo = 'pais'" in delete_sql
    assert "codigo = 'ES'" in delete_sql

    # INSERT con todos los valores
    assert "INSERT INTO param_paises" in insert_sql
    assert "'Portugal'" in insert_sql

    # UPDATE con todos los valores del estado anterior
    assert "UPDATE param_paises" in update_sql
    assert "nombre = 'Italia'" in update_sql
    assert "activo = 'True'" in update_sql
    assert "tipo = 'pais'" in update_sql
    assert "codigo = 'IT'" in update_sql


def test_rollback_sql_added_with_missing_key():
    rollback_service = RollbackService()

    diff = DiffResultDTO(
        added=[{"valor": "x"}], removed=[], changed=[]  # falta "clave"
    )

    sql = rollback_service.generate_rollback_sql(diff, "mi_tabla", key_fields=["clave"])

    assert sql[0].startswith("-- [AVISO]")


def test_rollback_sql_with_missing_before_data():
    rollback_service = RollbackService()

    diff = DiffResultDTO(
        added=[],
        removed=[],
        changed=[
            {"key": ("x",), "before": None, "after": {"clave": "x", "valor": "nuevo"}}
        ],
    )

    sql = rollback_service.generate_rollback_sql(diff, "mi_tabla", key_fields=["clave"])

    assert sql[0].startswith("-- [AVISO]")
