from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsTrackerABC

from .Options import Options


@dataclass
class OptionsTracker(OptionsTrackerABC[Options]):
    ...
