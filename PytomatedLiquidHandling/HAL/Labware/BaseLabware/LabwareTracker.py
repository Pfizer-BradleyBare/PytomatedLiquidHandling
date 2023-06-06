from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from . import LabwareABC
from dataclasses import dataclass


@dataclass
class LabwareTracker(UniqueObjectTrackerABC[LabwareABC]):
    pass
