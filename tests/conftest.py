from datetime import datetime

import pytest

from core.domain.dto.diff_result_dto import DiffResultDTO
from core.domain.models import ParamEntry, ParamSnapshot


@pytest.fixture
def build_snapshot():
    def _builder(entries: list) -> ParamSnapshot:
        return ParamSnapshot(
            table_name="config_servicio",
            timestamp=datetime(2024, 6, 1, 0, 0, 0),
            entries=[ParamEntry(values=e) for e in entries],
        )

    return _builder


@pytest.fixture
def diff_result_example():
    return DiffResultDTO(
        added=[{"clave": "nuevo", "valor": "x", "activo": True}],
        removed=[{"clave": "modo", "valor": "prod", "activo": True}],
        changed=[
            {
                "key": ("timeout",),
                "before": {"clave": "timeout", "valor": "30", "activo": True},
                "after": {"clave": "timeout", "valor": "45", "activo": True},
            }
        ],
    )


@pytest.fixture
def diff_compuesto_example():
    return DiffResultDTO(
        added=[{"tipo": "pais", "codigo": "ES", "nombre": "España", "activo": True}],
        removed=[
            {"tipo": "pais", "codigo": "PT", "nombre": "Portugal", "activo": True}
        ],
        changed=[
            {
                "key": ("pais", "IT"),
                "before": {
                    "tipo": "pais",
                    "codigo": "IT",
                    "nombre": "Italia",
                    "activo": True,
                },
                "after": {
                    "tipo": "pais",
                    "codigo": "IT",
                    "nombre": "Italia (nuevo)",
                    "activo": False,
                },
            }
        ],
    )
