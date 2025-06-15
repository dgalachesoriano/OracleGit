from core.domain.interfaces.database_connector import IDatabaseConnector
from typing import List, Dict


class MockDatabaseConnector(IDatabaseConnector):
    def fetch_table_data(self, table_name: str) -> List[Dict]:
        """
        Devuelve datos simulados para una tabla de parametría.
        Esto imita una consulta real a la BBDD.
        """

        if table_name == "config_servicio":
            return [
                {"clave": "timeout", "valor": "40", "activo": True},
                {"clave": "modo", "valor": "SAFE", "activo": True},
            ]

        elif table_name == "param_app":
            return [
                {"param": "MAX_USERS", "value": "100"},
                {"param": "ENV", "value": "DEV"},
            ]

        else:
            return []
