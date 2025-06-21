from datetime import datetime
from typing import Any, Dict, List

from core.domain.models import ParamEntry, ParamSnapshot


def snapshot_to_dict(snapshot: ParamSnapshot) -> Dict[str, Any]:
    """Convert a ParamSnapshot to a dictionary."""
    return {
        "table_name": snapshot.table_name,
        "timestamp": snapshot.timestamp.isoformat(),
        "entries": [entry.values for entry in snapshot.entries],
    }


def snapshot_from_dict(data: Dict[str, Any]) -> ParamSnapshot:
    timestamp = datetime.fromisoformat(data["timestamp"])
    entries = [ParamEntry(values=entry) for entry in data["entries"]]
    return ParamSnapshot(
        table_name=data["table_name"], timestamp=timestamp, entries=entries
    )
