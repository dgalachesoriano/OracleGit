from typing import Dict, List, Optional


class DiffResultDTO:
    def __init__(
        self,
        added: List[Dict],
        removed: List[Dict],
        changed: Optional[List[Dict]] = None,
    ):
        self.added = added
        self.removed = removed
        self.changed = changed or []

    def is_empty(self) -> bool:
        return not self.added and not self.removed and not self.changed

    def to_dict(self) -> Dict[str, List[Dict]]:
        return {"added": self.added, "removed": self.removed, "changed": self.changed}
