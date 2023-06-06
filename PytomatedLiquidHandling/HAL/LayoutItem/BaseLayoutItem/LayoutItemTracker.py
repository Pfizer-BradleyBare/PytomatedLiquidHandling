from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from . import LayoutItemABC
from dataclasses import dataclass


@dataclass
class LayoutItemTracker(UniqueObjectTrackerABC[LayoutItemABC]):
    pass
