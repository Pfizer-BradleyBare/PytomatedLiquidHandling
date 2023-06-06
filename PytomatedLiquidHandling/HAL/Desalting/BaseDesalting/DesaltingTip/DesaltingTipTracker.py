from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from dataclasses import dataclass
from .DesaltingTip import DesaltingTip


@dataclass
class DesaltingTipTracker(UniqueObjectTrackerABC[DesaltingTip]):
    ...
