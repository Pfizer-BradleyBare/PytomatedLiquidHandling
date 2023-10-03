from enum import Enum
from typing import Self, cast

from .Value import Value


class Property(Enum):
    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> Self:  # type: ignore
        for Item in cls:
            ReagentPropertyValueInstance = Item.value
            if not isinstance(ReagentPropertyValueInstance, Value):
                raise Exception(
                    "Your enum is wrong. All items must be ReagentPropertyValues"
                )
            ReagentPropertyValueInstance = cast(Value, ReagentPropertyValueInstance)
            if ReagentPropertyValueInstance.NumericValue == NumericKey:
                return Item
