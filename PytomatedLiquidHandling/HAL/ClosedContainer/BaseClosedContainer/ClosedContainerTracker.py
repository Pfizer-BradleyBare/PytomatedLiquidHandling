from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .ClosedContainerABC import ClosedContainerABC
from dataclasses import dataclass


@dataclass
class ClosedContainerTracker(UniqueObjectTrackerABC[ClosedContainerABC]):
    pass
