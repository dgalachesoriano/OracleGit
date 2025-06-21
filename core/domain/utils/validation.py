def validate_key_fields(snapshot_entries: list, key_fields: list[str]) -> bool:
    """
    Verifica que todos los registros tengan presentes los campos clave.
    """
    if not key_fields:
        return False

    return all(all(k in entry.values for k in key_fields) for entry in snapshot_entries)
