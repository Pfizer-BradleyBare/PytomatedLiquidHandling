from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from .PipetteTip import PipetteTip
from dataclasses import dataclass


@dataclass
class PipetteTipTracker(UniqueObjectTrackerABC[PipetteTip]):
    ...
