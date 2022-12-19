from enum import Enum

from .BaseSolutionProperty.SolutionProperty import SolutionPropertyValue


class LLDSolutionProperty(Enum):
    Normal = SolutionPropertyValue(1, 0, 0)
    Organic = SolutionPropertyValue(1, 0, 0)

    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> LLDSolutionProperty:  # type: ignore
        for Item in LLDSolutionProperty:
            if Item.value.GetNumericValue() == NumericKey:
                return Item
