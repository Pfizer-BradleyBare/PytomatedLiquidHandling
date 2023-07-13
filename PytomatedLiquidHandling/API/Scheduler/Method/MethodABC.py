from dataclasses import dataclass, field
from enum import Enum
from typing import Type

import treelib

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
    ExecutedStepTrackerInstance: StepTracker = field(
        init=False, default_factory=StepTracker
    )
    MethodStepPathways: list[StepTracker] = field(init=False, default_factory=list)

    def __post_init__(self):
        if self.Simulate == True:
            self.Priority = self.PriorityOptions.NonStop

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

            self.MethodStepPathways.append(StepTrackerInstance)
        # Take the step tree and create discrete lists of step for each pathway.

    def PreExecute(self, OrchastratorInstance: Orchastrator):
        for StepTrackerInstance in self.MethodStepPathways:
            for StepInstance in StepTrackerInstance.GetObjectsAsList():
                if StepInstance.ExecuteComplete == True:
                    if (
                        self.ExecutedStepTrackerInstance.IsTracked(
                            StepInstance.UniqueIdentifier
                        )
                        == False
                    ):
                        self.ExecutedStepTrackerInstance.LoadSingle(StepInstance)
            # add to executed tracker

            for StepInstance in StepTrackerInstance.GetObjectsAsList():
                if (
                    self.ExecutedStepTrackerInstance.IsTracked(
                        StepInstance.UniqueIdentifier
                    )
                    == True
                ):
                    StepTrackerInstance.UnloadSingle(StepInstance)
            # remove from each list.

            ExecutionBlocks: dict[str | int, list[Type[StepABC]]] = dict()
            for StepInstance in StepTrackerInstance.GetObjectsAsList():
                ExecutionBlocks[
                    StepInstance.UniqueIdentifier
                ] = StepInstance.StepPreExecuteBlocks
            # get our execution blocks

            TimeToStep = 0
            for StepInstance in StepTrackerInstance.GetObjectsAsList():
                StepBlocks = sum(
                    [
                        ExecutionBlocks[Key]
                        for Key in ExecutionBlocks
                        if Key != StepInstance.UniqueIdentifier
                    ],
                    [],
                )

                if type(StepInstance) in StepBlocks:
                    continue

                TimeToStep += StepInstance.PreExecuteTime() + StepInstance.ExecuteTime()

                StepInstance.PreExecute(
                    self.Simulate,
                    OrchastratorInstance,
                    self.UtilitiesInstance,
                    TimeToStep,
                )
            # do the EQ
        # first we need to try to do our pre-execution for as many steps as possible.
        # We always iterate over all steps to find PreExecutions that are meant to run during timer countdowns

    def Execute(self, OrchastratorInstance: Orchastrator):
        TimeKeeper = float("inf")
        FastestPathway: StepTracker | None = None
        for StepTrackerInstance in self.MethodStepPathways:
            PathwayTime = 0
            for StepInstance in StepTrackerInstance.GetObjectsAsList():
                if StepInstance.HasTimer() == True:
                    break
                PathwayTime += (
                    StepInstance.PreExecuteTime() + StepInstance.ExecuteTime()
                )

            if PathwayTime < TimeKeeper:
                FastestPathway = StepTrackerInstance
        # find the fastest path
