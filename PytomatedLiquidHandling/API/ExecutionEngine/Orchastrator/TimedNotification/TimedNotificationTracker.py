from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .TimedNotification import TimedNotification


@dataclass
class TimedNotificationTracker(UniqueObjectTrackerABC[TimedNotification]):
    ...
