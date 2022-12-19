from enum import Enum

from .BaseSolutionProperty.SolutionProperty import SolutionPropertyValue


class HomogeneitySolutionProperty(Enum):
    Homogenous = SolutionPropertyValue(1, 0, 0)
    Emulsion = SolutionPropertyValue(1, 0, 0)
    Suspension = SolutionPropertyValue(1, 0, 0)
    Heterogenous = SolutionPropertyValue(1, 0, 0)

    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> HomogeneitySolutionProperty:  # type: ignore
        for Item in HomogeneitySolutionProperty:
            if Item.value.GetNumericValue() == NumericKey:
                return Item
