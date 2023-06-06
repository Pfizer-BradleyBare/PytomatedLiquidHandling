from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .Tip import Tip
from dataclasses import dataclass


@dataclass
class TipTracker(UniqueObjectTrackerABC[Tip]):
    ...
