from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .Container import Container


@dataclass
class ContainerTracker(UniqueObjectTrackerABC[Container]):
    ...
