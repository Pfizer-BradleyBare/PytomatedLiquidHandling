from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .WellEquation import WellEquation


@dataclass
class WellEquationTracker(NonUniqueObjectTrackerABC[WellEquation]):
    pass
