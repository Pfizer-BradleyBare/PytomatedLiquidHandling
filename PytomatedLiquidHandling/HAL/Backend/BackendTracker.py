from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from ...Driver.Tools.AbstractClasses import BackendABC


@dataclass
class BackendTracker(UniqueObjectTrackerABC[BackendABC]):
    ...
