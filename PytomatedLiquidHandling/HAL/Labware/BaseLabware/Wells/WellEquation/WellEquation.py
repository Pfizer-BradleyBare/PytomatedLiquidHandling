from ......Tools.AbstractClasses import NonUniqueObjectABC
from dataclasses import dataclass, field


@dataclass
class WellEquation(NonUniqueObjectABC):
    Identifier: str | int = field(init=False, default="Well Equation")
    SegmentHeight: float
    SegmentEquation: str
