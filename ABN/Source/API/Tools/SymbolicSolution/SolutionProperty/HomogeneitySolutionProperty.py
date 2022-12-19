from enum import Enum
from typing import Self

from .BaseSolutionProperty.SolutionProperty import SolutionPropertyValue


class HomogeneitySolutionProperty(Enum):
    Homogenous = SolutionPropertyValue(1, 0, 0)
    Emulsion = SolutionPropertyValue(1, 0, 0)
    Suspension = SolutionPropertyValue(1, 0, 0)
    Heterogenous = SolutionPropertyValue(1, 0, 0)

    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> Self:  # type: ignore
        for Item in HomogeneitySolutionProperty:
            if Item.value.GetNumericValue() == NumericKey:
                return Item
