from dataclasses import dataclass, field
from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from .Step import StepTracker


@dataclass
class MethodABC(UniqueObjectABC):
    class PriorityOptions(Enum):
        NonStop = 2
        Critical = 1
        Normal = 0

    Simulate: bool
    Priority: PriorityOptions
    StepTrackerInstance: StepTracker
    ExecutedStepTrackerInstance: StepTracker = field(init=False, default=StepTracker())

    def ExecuteStep(self):
        ...
