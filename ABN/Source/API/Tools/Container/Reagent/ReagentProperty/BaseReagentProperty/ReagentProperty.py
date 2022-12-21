from enum import Enum
from typing import Self


class ReagentProperty(Enum):
    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> Self:  # type: ignore
        for Item in Self:
            if Item.value.GetNumericValue() == NumericKey:
                return Item
