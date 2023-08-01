from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .LoadedLayoutItem import LoadedLayoutItem


@dataclass
class LoadedLayoutItemTracker(NonUniqueObjectTrackerABC[LoadedLayoutItem]):
    ...
