from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .IMCSDesaltingABC import IMCSDesaltingABC
from dataclasses import dataclass


@dataclass
class IMCSDesaltingTracker(UniqueObjectTrackerABC[IMCSDesaltingABC]):
    ...
