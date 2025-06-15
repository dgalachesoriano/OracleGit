from abc import ABC, abstractmethod
from core.domain.models import ParamSnapshot
from core.domain.dto.diff_result_dto import DiffResultDTO
from typing import List


class IDiffService(ABC):
    @abstractmethod
    def compare_snapshots(self, old: ParamSnapshot, new: ParamSnapshot, key_fields: List[str]) -> DiffResultDTO:
      pass
