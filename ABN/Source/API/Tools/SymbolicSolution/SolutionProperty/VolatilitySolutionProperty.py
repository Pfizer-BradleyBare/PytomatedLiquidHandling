from enum import Enum
from typing import Self

from .BaseSolutionProperty.SolutionProperty import SolutionPropertyValue


class VolatilitySolutionProperty(Enum):
    Low = SolutionPropertyValue(1, 0, 0)
    Medium = SolutionPropertyValue(1, 0, 0)
    High = SolutionPropertyValue(1, 0, 0)

    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> Self:  # type: ignore
        for Item in VolatilitySolutionProperty:
            if Item.value.GetNumericValue() == NumericKey:
                return Item
