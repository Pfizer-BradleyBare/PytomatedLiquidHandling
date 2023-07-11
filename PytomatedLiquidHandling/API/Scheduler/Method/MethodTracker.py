from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .MethodABC import MethodABC


@dataclass
class MethodTracker(UniqueObjectTrackerABC[MethodABC]):
    ...
