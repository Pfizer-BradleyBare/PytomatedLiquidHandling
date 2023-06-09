from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from . import ClosedContainerABC
from dataclasses import dataclass


@dataclass
class ClosedContainerTracker(UniqueObjectTrackerABC[ClosedContainerABC]):
    pass
