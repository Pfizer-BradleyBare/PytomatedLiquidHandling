from enum import Enum
from typing import Self

from .BaseSolutionProperty.SolutionProperty import SolutionPropertyValue


class LLDSolutionProperty(Enum):
    Normal = SolutionPropertyValue(1, 0, 0)
    Organic = SolutionPropertyValue(1, 0, 0)

    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> Self:  # type: ignore
        for Item in LLDSolutionProperty:
            if Item.value.GetNumericValue() == NumericKey:
                return Item
