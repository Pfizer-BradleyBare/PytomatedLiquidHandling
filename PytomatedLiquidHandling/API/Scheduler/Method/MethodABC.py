from dataclasses import dataclass, field
from enum import Enum
from itertools import permutations
from typing import Type

import treelib

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .Step import StepABC, StepTracker


@dataclass
class MethodABC(UniqueObjectABC):
    Simulate: bool

    class StateOptions(Enum):
        Queued = 0
        Running = 1
        Error = 2
        Complete = 3

    State: StateOptions = field(init=False, default=StateOptions.Queued)

    StepTreeInstance: treelib.Tree
    FlattenedMethod: StepTracker = field(init=False, default_factory=StepTracker)

    def __post_init__(self):
        MethodPathways: list[StepTracker] = list()
        for StepPathway in self.StepTreeInstance.paths_to_leaves():
            StepTrackerInstance = StepTracker()

            for StepID in StepPathway:
                Node = self.StepTreeInstance.get_node(StepID)
                if not isinstance(Node, treelib.Node):
                    raise Exception("")
                # bad typing in treelib so we have to do this

                Step = Node.data
                if not isinstance(Step, StepABC):
                    raise Exception("")
                # bad typing in treelib so we have to do this

                StepTrackerInstance.LoadSingle(Step)

            MethodPathways.append(StepTrackerInstance)
        # Take the step tree and create discrete lists of step for each pathway.
