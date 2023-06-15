from ....Tools.AbstractClasses import UniqueObjectTrackerABC, UniqueObjectABC
from .Step import StepTracker
from dataclasses import dataclass
from enum import Enum


@dataclass
class MethodABC(UniqueObjectABC):
    class PriorityOptions(Enum):
        NonStop = 2
        Critical = 1
        Normal = 0

    Simulate: bool
    Priority: PriorityOptions
    StepTrackerInstance: StepTracker

    def ExecuteStep(self):
        ...
