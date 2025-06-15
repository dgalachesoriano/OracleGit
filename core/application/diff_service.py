from core.domain.interfaces.diff_service import IDiffService
from core.domain.dto.diff_result_dto import DiffResultDTO
from core.domain.models import ParamSnapshot
from typing import List, Dict, Tuple


class DiffService(IDiffService):
    def compare_snapshots(
        self,
        old: ParamSnapshot,
        new: ParamSnapshot,
        key_fields: List[str]
    ) -> DiffResultDTO:

        def extract_key(entry: Dict) -> Tuple:
            return tuple(entry.get(field) for field in key_fields)

        old_map = {extract_key(e.values): e.values for e in old.entries}
        new_map = {extract_key(e.values): e.values for e in new.entries}

        added = []
        removed = []
        changed = []

        all_keys = set(old_map.keys()).union(new_map.keys())

        for key in all_keys:
            old_val = old_map.get(key)
            new_val = new_map.get(key)

            if old_val and not new_val:
                removed.append(old_val)
            elif new_val and not old_val:
                added.append(new_val)
            elif old_val != new_val:
                # Cambió algún valor (aunque tiene la misma clave)
                changed.append({
                    "key": key,
                    "before": old_val,
                    "after": new_val
                })

        return DiffResultDTO(added=added, removed=removed, changed=changed)
