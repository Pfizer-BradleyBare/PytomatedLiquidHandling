from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .TempControlDevice import TempControlDevice


@dataclass
class TempControlDeviceTracker(UniqueObjectTrackerABC[TempControlDevice]):
    ...
