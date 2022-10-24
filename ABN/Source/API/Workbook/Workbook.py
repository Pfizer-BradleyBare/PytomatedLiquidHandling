import os
from enum import Enum
import threading

from ...AbstractClasses import ObjectABC
from .Block import BlockTracker
from ...Tools import Tree
from .Worklist import Worklist
from .Solution import SolutionTracker
from ...API.Tools.Container import ContainerTracker
from ...API.Tools.Context import (
    ContextTracker,
    Context,
    WellFactorTracker,
    WellSequencesTracker,
    WellSequences,
    WellFactor,
)
from ..Tools.Timer import TimerTracker
from ...HAL.Tools import DeckLoadingItemTracker

from ...Server.Tools import LOG
from ...Server.Tools.HalInstance import HalInstance
from ...Server.Tools import AliveStateFlag


class WorkbookStates(Enum):
    # NOTE Fun Fact. The workbook states only matter for the Run type below.
    Queued = "Queued"
    Running = "Running"
    Paused = "Paused"  # The user paused this method manually
    Waiting = "Waiting"  # Something occured so the method is waiting on the user
    Stopped = "Stopped"  # The user stopped the method but it is still in the list. This allows
    # the user to remove plates and all that jazz
    # Killed = "Killed" #The method has been removed from the tracker. It no longer exists


class WorkbookRunTypes(Enum):
    Test = "Test"  # This is a single programmatic test to check method is compatible with system
    Prep = "Prep"  # This will test with all samples added then generate a preparation list for the user
    PreRun = "PreRun"  # This is the first step of Run
    Run = "Run"  # This will queue to run on the system


# NOTE
#   Workbook contain information about the block pathways, worklist, and solutions
#   A workbook should, ideally, handle the starting and stopping of block pathways
#   Workbook execution should occur as a thread that relies on a thread lock to execute.
#   The workbook thread lock is used to pause workbook execution entirely?
#   The workbook should determine which pathway should be currently executed.
#   How the heck am I going to do this????
#
# ok so this is my plan:
# Thw thread will only read steps. It will not modify the block tracker list at all.
# All modification must occur by the workbook somehow


class Workbook(ObjectABC):
    def __init__(
        self,
        RunType: WorkbookRunTypes,
        MethodPath: str,
        MethodTree: Tree,
        WorklistInstance: Worklist,
        SolutionTrackerInstance: SolutionTracker,
        DeckLoadingItemTrackerInstance: DeckLoadingItemTracker,
    ):

        # Variables
        self.RunType: WorkbookRunTypes = RunType
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.State: WorkbookStates = WorkbookStates.Queued

        # Trackers
        self.MethodTree: Tree = MethodTree
        self.ExecutedBlocksTrackerInstance: BlockTracker = BlockTracker()
        self.WorklistInstance: Worklist = WorklistInstance
        self.SolutionTrackerInstance: SolutionTracker = SolutionTrackerInstance
        self.DeckLoadingItemTrackerInstance: DeckLoadingItemTracker = (
            DeckLoadingItemTrackerInstance
        )
        self.ContainerTrackerInstance: ContainerTracker = ContainerTracker()
        self.ActiveContexts: ContextTracker = ContextTracker()
        self.InactiveContexts: ContextTracker = ContextTracker()
        self.TimerTrackerInstance: TimerTracker = TimerTracker()

        LOG.debug(
            "The following method tree was determined for %s: \n%s",
            self.MethodName,
            self.MethodTree.GetCurrentNode(),
        )

        # Do the necessary init function.
        # Why do it here? Because all init is handled inside the init function for simplicity sake
        WorkbookInit(self)

    def GetName(self) -> str:
        return self.MethodName

    def GetPath(self) -> str:
        return self.MethodPath

    def GetRunType(self) -> WorkbookRunTypes:
        return self.RunType

    def GetState(self) -> WorkbookStates:
        return self.State

    def GetExecutedBlockTracker(self) -> list[BlockTracker]:
        return self.ExecutedBlocksTrackerInstance

    def GetWorklist(self) -> Worklist:
        return self.WorklistInstance

    def GetSolutionTracker(self) -> SolutionTracker:
        return self.SolutionTrackerInstance

    def GetContainerTracker(self) -> ContainerTracker:
        return self.ContainerTrackerInstance

    def GetActiveContexts(self) -> ContextTracker:
        return self.ActiveContexts

    def GetInactiveContexts(self) -> ContextTracker:
        return self.InactiveContexts

    def GetTimerTracker(self) -> TimerTracker:
        return self.TimerTrackerInstance

    def GetWorkbookProcessorThread(self) -> threading.Thread:
        return self.WorkbookProcessorThread

    def GetProcessingLock(self) -> threading.Lock:
        return self.ProcessingLock


def WorkbookProcessor(WorkbookInstance: Workbook):

    HalInstance

    while True:

        WorkbookInstance.ProcessingLock.acquire()
        WorkbookInstance.ProcessingLock.release()
        # The processing lock is used as a pause button to control which workbook executes.
        # During acquire we wait for the thread to be unpaused.
        # We immediately release so we do not stall the main process

        if AliveStateFlag.AliveStateFlag is False:
            break

        # somehow figure out the processing

        # do processing here


def WorkbookInit(WorkbookInstance: Workbook):

    # Check runtype. We will determine the starting well here
    if WorkbookInstance.GetRunType() == WorkbookRunTypes.Run:
        pass
    else:
        StartingWell = 1

    # Set Initial Active Context
    AspirateWellSequencesTrackerInstance = WellSequencesTracker()
    DispenseWellSequencesTrackerInstance = WellSequencesTracker()

    WellFactorsTrackerInstance = WellFactorTracker()

    for SampleNumber in range(0, WorkbookInstance.GetWorklist().GetNumSamples()):
        WellNumber = StartingWell + SampleNumber

        WellSequencesInstance = WellSequences(WellNumber, [WellNumber])
        WellFactorInstance = WellFactor(WellNumber, 1)

        AspirateWellSequencesTrackerInstance.ManualLoad(WellSequencesInstance)
        DispenseWellSequencesTrackerInstance.ManualLoad(WellSequencesInstance)

        WellFactorsTrackerInstance.ManualLoad(WellFactorInstance)

    WorkbookInstance.GetActiveContexts().ManualLoad(
        Context(
            ":__StartingContext__",
            AspirateWellSequencesTrackerInstance,
            DispenseWellSequencesTrackerInstance,
            WellFactorsTrackerInstance,
        )
    )

    # Thread: Create and start
    WorkbookInstance.WorkbookProcessorThread: threading.Thread = threading.Thread(
        name=WorkbookInstance.MethodName + "->" + WorkbookInstance.RunType.value,
        target=WorkbookProcessor,
        args=(WorkbookInstance,),  # args must be tuple hence the empty second argument
    )
    WorkbookInstance.ProcessingLock: threading.Lock = threading.Lock()
    WorkbookInstance.ProcessingLock.acquire()
    WorkbookInstance.WorkbookProcessorThread.start()
