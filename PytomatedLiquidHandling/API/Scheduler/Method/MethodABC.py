from dataclasses import dataclass, field
from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from .Step import StepTracker


@dataclass
class MethodABC(UniqueObjectABC):
    Simulate: bool

    class PriorityOptions(Enum):
        NonStop = 2
        Critical = 1
        Normal = 0

    Priority: PriorityOptions

    class StateOptions(Enum):
        Queued = 0
        Running = 1
        Waiting = 2
        Error = 3

    State: StateOptions = field(init=False, default=StateOptions.Queued)

    StepTrackerInstance: StepTracker
    ExecutedStepTrackerInstance: StepTracker = field(init=False, default=StepTracker())

    def __post_init__(self):
        if self.Simulate == True:
            self.Priority = self.PriorityOptions.NonStop

    def ExecuteStep(self):
        ...
