from dataclasses import dataclass, field
from enum import Enum

import treelib

from PytomatedLiquidHandling.API.Tools import ResourceReservation
from PytomatedLiquidHandling.HAL import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

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

    StepTreeInstance: treelib.Tree

    ExecutedStepTrackerInstance: StepTracker = field(init=False, default=StepTracker())
    MethodStepPathways: list[StepTracker] = field(init=False, default_factory=list)

    def __post_init__(self):
        if self.Simulate == True:
            self.Priority = self.PriorityOptions.NonStop

        for StepPathway in self.StepTreeInstance.paths_to_leaves():
            StepTrackerInstance = StepTracker()
            StepTrackerInstance.LoadList([Node.data for Node in StepPathway])
            self.MethodStepPathways.append(StepTrackerInstance)
        # Take the step tree and create discrete lists of step for each pathway.

    def ExecuteStep(
        self,
        HALInstance: HAL,
        ResourceReservationTrackerInstance: ResourceReservation.ResourceReservationTracker,
    ):
        ...
