from dataclasses import dataclass, field
from enum import Enum
from typing import Type

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
    ExecutedStepTrackerInstance: StepTracker = field(
        init=False, default_factory=StepTracker
    )
    MethodStepPathways: list[StepTracker] = field(init=False, default_factory=list)
    CurrentPathway: StepTracker | None = field(init=False, default=None)

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

    @staticmethod
    def IsStepBlocked(StepInstance: StepABC, StepTrackerInstance: StepTracker) -> bool:
        ExecutionBlocks: dict[str | int, list[Type[StepABC]]] = dict()
        for Step in StepTrackerInstance.GetObjectsAsList():
            ExecutionBlocks[Step.UniqueIdentifier] = Step.StepPreExecuteBlocks
        # get our execution blocks

        StepBlocks = sum(
            [
                ExecutionBlocks[Key]
                for Key in ExecutionBlocks
                if Key != StepInstance.UniqueIdentifier
            ],
            [],
        )

        if type(StepInstance) in StepBlocks:
            return True
        else:
            return False

    @staticmethod
    def IsPathwayActive(StepTrackerInstance: StepTracker) -> bool:
        if StepTrackerInstance.GetNumObjects() != 0:
            return not MethodABC.IsStepBlocked(
                StepTrackerInstance.GetObjectsAsList()[0], StepTrackerInstance
            )
        return False

    def IsActive(self) -> bool:
        for StepTrackerInstance in self.MethodStepPathways:
            if not MethodABC.IsPathwayActive(StepTrackerInstance):
                return False
        return True

    def PreExecuteSteps(self, OrchastratorInstance: Orchastrator):
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

            PathwaySleepTime = 0
            for (
                TimerInstance
            ) in self.UtilitiesInstance.TimerTrackerInstance.GetObjectsAsList():
                if StepTrackerInstance.IsTracked(TimerInstance.UniqueIdentifier):
                    if TimerInstance.GetRemainingTime() > PathwaySleepTime:
                        PathwaySleepTime = TimerInstance.GetRemainingTime()
            # get sleeping time of pathway if sleeping is occuring.

            TimeToStep = 0
            for StepInstance in StepTrackerInstance.GetObjectsAsList():
                TimeToStep += StepInstance.PreExecuteTime() + StepInstance.ExecuteTime()

                if MethodABC.IsStepBlocked(StepInstance, StepTrackerInstance):
                    continue

                if StepInstance.PreExecuteTime() <= PathwaySleepTime:
                    StepInstance.PreExecute(
                        self.Simulate,
                        OrchastratorInstance,
                        self.UtilitiesInstance,
                        TimeToStep,
                    )
            # do the EQ
        # first we need to try to do our pre-execution for as many steps as possible.
        # We always iterate over all steps to find PreExecutions that are meant to run during timer countdowns

    def ExecuteNextStep(self, OrchastratorInstance: Orchastrator):
        if self.IsActive() == False:
            return

        if self.CurrentPathway is None:
            TimeKeeper = float("inf")
            for StepTrackerInstance in self.MethodStepPathways:
                PathwayTime = 0
                for StepInstance in StepTrackerInstance.GetObjectsAsList():
                    if StepInstance.HasTimer() == True:
                        break
                    PathwayTime += (
                        StepInstance.PreExecuteTime() + StepInstance.ExecuteTime()
                    )

                if (
                    PathwayTime <= TimeKeeper
                    and MethodABC.IsPathwayActive(StepTrackerInstance) == True
                ):
                    self.CurrentPathway = StepTrackerInstance
            # find the fastest path

        if self.CurrentPathway is None:
            return

        StepInstance = self.CurrentPathway.GetObjectsAsList()[0]

        # it is assumed that pre-execution has already occured.
        StepInstance.Execute(
            self.Simulate, OrchastratorInstance, self.UtilitiesInstance
        )
