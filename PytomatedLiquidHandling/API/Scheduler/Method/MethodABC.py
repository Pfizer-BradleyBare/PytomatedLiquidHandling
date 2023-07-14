from dataclasses import dataclass, field
from enum import Enum
from typing import Type
from itertools import permutations
import treelib

from PytomatedLiquidHandling.Tools import Logger
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ..Orchastrator import Orchastrator
from .Step import StepABC, StepTracker
from .Utilities import Utilities


@dataclass
class MethodABC(UniqueObjectABC):
    Simulate: bool
    UtilitiesInstance: Utilities

    class PriorityOptions(Enum):
        NonStop = 2
        Critical = 1
        Normal = 0

    Priority: PriorityOptions

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

        while len(MethodPathways) != 0:
            PartialPathways: list[tuple[float, float, float, list[StepABC]]] = list()
            for StepTrackerInstance in MethodPathways[:]:
                PartialPathway: list[StepABC] = list()
                for StepInstance in StepTrackerInstance.GetObjectsAsList():
                    PartialPathway.append(StepInstance)

                    if StepInstance.IsTimed() == True:
                        break

                StepTrackerInstance.UnloadList(PartialPathway)
                if StepTrackerInstance.GetNumObjects() == 0:
                    MethodPathways.remove(StepTrackerInstance)

                Partial = StepTracker()
                Partial.LoadList(
                    PartialPathway[:-1]
                )  # get time of all but the timed step
                Full = StepTracker()
                Full.LoadList(PartialPathway)  # get time of all but the timed step

                PartialPathways.append(
                    (
                        Full.GetExecutionTime(),
                        Partial.GetExecutionTime(),
                        PartialPathway[-1].GetExecuteTime(),
                        PartialPathway,
                    )
                )

            PathTimeSorted = sorted(PartialPathways, key=lambda x: x[1])
            # time to execute path WITHOUT the timed step

            PartialPathwayPermutations = permutations(PathTimeSorted)

            FavoritePermutation = tuple(PathTimeSorted)
            # default to the time sorted as favorate
            for Permutation in PartialPathwayPermutations:
                ...
