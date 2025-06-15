import os
from typing import Dict, List

import oracledb

from core.domain.interfaces.database_connector import IDatabaseConnector


class OracleDatabaseConnector(IDatabaseConnector):
    def __init__(self, user: str, password: str, dsn: str):
        self.user = user
        self.password = password
        self.dsn = dsn

    def fetch_table_data(self, table_name: str) -> List[Dict]:
        connection = oracledb.connect(
            user=self.user, password=self.password, dsn=self.dsn
        )
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [col[0].lower() for col in cursor.description]
        rows = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        connection.close()

        return result
