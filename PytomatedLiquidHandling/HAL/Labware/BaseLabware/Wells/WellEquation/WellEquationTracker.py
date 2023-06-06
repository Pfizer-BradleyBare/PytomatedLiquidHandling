from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .WellEquation import WellEquation
from dataclasses import dataclass


@dataclass
class WellEquationTracker(NonUniqueObjectTrackerABC[WellEquation]):
    pass
