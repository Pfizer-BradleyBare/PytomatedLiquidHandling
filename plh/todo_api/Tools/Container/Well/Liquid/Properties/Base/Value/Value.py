from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Value:
    _NumericValueCounter: ClassVar[int] = 1
    NumericValue: int = field(init=False)
    Weight: int
    MinAspirateMix: int
    MinDispenseMix: int

    def __post_init__(self):
        self.NumericValue = Value._NumericValueCounter
        Value._NumericValueCounter += 1
