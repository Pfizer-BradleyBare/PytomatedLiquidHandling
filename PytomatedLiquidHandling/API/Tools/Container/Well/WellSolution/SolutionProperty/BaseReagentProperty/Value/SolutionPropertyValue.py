from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class SolutionPropertyValue:
    _NumericValueCounter: ClassVar[int] = 1
    NumericValue: int = field(init=False)
    Weight: int
    MinAspirateMix: int
    MinDispenseMix: int

    def __post_init__(self):
        self.NumericValue = SolutionPropertyValue._NumericValueCounter
        SolutionPropertyValue._NumericValueCounter += 1
