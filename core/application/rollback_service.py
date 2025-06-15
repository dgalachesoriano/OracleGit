from core.domain.interfaces.rollback_service import IRollbackService
from core.domain.dto.diff_result_dto import DiffResultDTO
from typing import List, Dict


class RollbackService(IRollbackService):
    def generate_rollback_sql(
        self,
        diff: DiffResultDTO,
        table_name: str,
        key_fields: List[str]
    ) -> List[str]:
        sql_statements = []

        def where_clause(entry: Dict) -> str:
            return " AND ".join(f"{k} = '{entry[k]}'" for k in key_fields if k in entry)

        # Registros añadidos → DELETE
        for row in diff.added:
            if all(k in row for k in key_fields):
                sql = f"DELETE FROM {table_name} WHERE {where_clause(row)};"
            else:
                sql = f"-- [AVISO] Clave incompleta para DELETE en fila añadida: {row}"
            sql_statements.append(sql)

        # Registros eliminados → INSERT
        for row in diff.removed:
            columns = ", ".join(row.keys())
            values = ", ".join(f"'{v}'" for v in row.values())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            sql_statements.append(sql)

        # Registros modificados → UPDATE
        for change in diff.changed:
            before = change.get("before")
            if before and all(k in before for k in key_fields):
                set_clause = ", ".join(f"{col} = '{val}'" for col, val in before.items())
                sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause(before)};"
            else:
                sql = f"-- [AVISO] Clave incompleta para UPDATE: {change}"
            sql_statements.append(sql)

        return sql_statements
