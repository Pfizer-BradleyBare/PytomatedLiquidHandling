from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .SolutionProperty import SolutionCategory


@dataclass
class WellSolution(UniqueObjectABC):
    Volume: float

    SolutionCategoryInstance: SolutionCategory
