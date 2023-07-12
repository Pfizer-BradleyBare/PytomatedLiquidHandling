from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectABC


@dataclass
class WellEquation(NonUniqueObjectABC):
    Identifier: str | int = field(init=False, default="Well Equation")
    SegmentHeight: float
    SegmentEquation: str
