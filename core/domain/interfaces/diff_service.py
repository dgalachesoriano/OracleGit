from abc import ABC, abstractmethod
from typing import List

from core.domain.dto.diff_result_dto import DiffResultDTO
from core.domain.models import ParamSnapshot


class IDiffService(ABC):
    @abstractmethod
    def compare_snapshots(
        self, old: ParamSnapshot, new: ParamSnapshot, key_fields: List[str]
    ) -> DiffResultDTO:
        pass
