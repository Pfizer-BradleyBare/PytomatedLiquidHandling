from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .Timer import Timer


@dataclass
class TimerTracker(UniqueObjectTrackerABC[Timer]):
    ...
