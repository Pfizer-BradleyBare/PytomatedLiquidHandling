from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .TempControlDevice import TempControlDevice
from dataclasses import dataclass


@dataclass
class TempControlDeviceTracker(UniqueObjectTrackerABC[TempControlDevice]):
    ...
