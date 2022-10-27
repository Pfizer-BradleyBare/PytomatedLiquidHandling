import os
from enum import Enum
import threading

from ..Blocks import MergePlates, Incubate, SplitPlate, Finish

from ...AbstractClasses import ObjectABC
from .Block import BlockTracker, Block
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
        MethodBlocksTrackerInstance: BlockTracker,
        WorklistInstance: Worklist,
        SolutionTrackerInstance: SolutionTracker,
        DeckLoadingItemTrackerInstance: DeckLoadingItemTracker,
        PreprocessingBlocksTrackerInstance: BlockTracker,
    ):

        # Variables
        self.RunType: WorkbookRunTypes = RunType
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.State: WorkbookStates = WorkbookStates.Queued
        self.ExecutingContextInstance: Context
        self.MethodTreeRoot: Block = MethodBlocksTrackerInstance.GetObjectsAsList()[0]
        self.StartingWell: int

        # Trackers
        self.MethodBlocksTrackerInstance: BlockTracker = MethodBlocksTrackerInstance
        self.ExecutedBlocksTrackerInstance: BlockTracker = BlockTracker()
        self.PreprocessingBlocksTrackerInstance: BlockTracker = (
            PreprocessingBlocksTrackerInstance
        )
        self.WorklistInstance: Worklist = WorklistInstance
        self.SolutionTrackerInstance: SolutionTracker = SolutionTrackerInstance
        self.DeckLoadingItemTrackerInstance: DeckLoadingItemTracker = (
            DeckLoadingItemTrackerInstance
        )
        self.ContainerTrackerInstance: ContainerTracker = ContainerTracker()
        self.ContextTrackerInstance: ContextTracker = ContextTracker()
        self.InactiveContextTrackerInstance: ContextTracker = ContextTracker()
        self.TimerTrackerInstance: TimerTracker = TimerTracker()

        LOG.debug(
            "The following method tree was determined for %s: \n%s",
            self.MethodName,
            self.MethodTreeRoot,
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

    def GetMethodTreeRoot(self) -> Block:
        return self.MethodTreeRoot

    def GetStartingWell(self) -> int:
        return self.StartingWell

    def GetMethodBlocksTracker(self) -> BlockTracker:
        return self.MethodBlocksTrackerInstance

    def GetExecutedBlocksTracker(self) -> BlockTracker:
        return self.ExecutedBlocksTrackerInstance

    def GetPreprocessingBlocksTracker(self) -> BlockTracker:
        return self.PreprocessingBlocksTrackerInstance

    def GetWorklist(self) -> Worklist:
        return self.WorklistInstance

    def GetSolutionTracker(self) -> SolutionTracker:
        return self.SolutionTrackerInstance

    def GetContainerTracker(self) -> ContainerTracker:
        return self.ContainerTrackerInstance

    def GetContextTracker(self) -> ContextTracker:
        return self.ContextTrackerInstance

    def GetInactiveContextTracker(self) -> ContextTracker:
        return self.InactiveContextTrackerInstance

    def GetExecutingContext(self) -> Context:
        return self.ExecutingContextInstance

    def SetExecutingContext(self, ContextInstance: Context) -> None:
        self.ExecutingContextInstance = ContextInstance

    def GetTimerTracker(self) -> TimerTracker:
        return self.TimerTrackerInstance

    def GetWorkbookProcessorThread(self) -> threading.Thread:
        return self.WorkbookProcessorThread

    def GetProcessingLock(self) -> threading.Lock:
        return self.ProcessingLock


def WorkbookProcessor(WorkbookInstance: Workbook):

    ContextTrackerInstance = WorkbookInstance.GetContextTracker()
    InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()
    ExecutedBlocksTrackerInstance = WorkbookInstance.GetExecutedBlocksTracker()
    PreprocessingBlocksTrackerInstance = (
        WorkbookInstance.GetPreprocessingBlocksTracker()
    )

    CurrentExecutingBlock: Block = WorkbookInstance.GetMethodTreeRoot()
    CurrentExecutingBlock.Process(WorkbookInstance, HalInstance)
    ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
    # Do the first step processing here. First step is always a plate step.

    while True:

        def ListInList(List, InList) -> bool:
            for Item in List:
                if Item not in InList:
                    return False
            return True

        if (
            ListInList(
                WorkbookInstance.GetMethodBlocksTracker().GetObjectsAsList(),
                ExecutedBlocksTrackerInstance.GetObjectsAsList(),
            )
            is True
        ):
            return
        # First thing to do is check that all blocks have been executed.

        WorkbookInstance.ProcessingLock.acquire()
        WorkbookInstance.ProcessingLock.release()
        if AliveStateFlag.AliveStateFlag is False:
            # Do some workbook save state stuff here
            return
        # The processing lock is used as a pause button to control which workbook executes.
        # During acquire we wait for the thread to be unpaused.
        # We immediately release so we do not stall the main process
        # After release we must check that the server still wants to execute. If not, we do some save state stuff then kill the thread.

        ConfirmedPreprocessingBlockInstances: list[Block] = list()
        for (
            PreprocessingBlockInstance
        ) in PreprocessingBlocksTrackerInstance.GetObjectsAsList():

            SearchBlockInstance = PreprocessingBlockInstance

            while True:
                SearchBlockInstance = SearchBlockInstance.GetParentNode()

                if SearchBlockInstance is None:
                    ConfirmedPreprocessingBlockInstances.append(
                        PreprocessingBlockInstance
                    )
                    PreprocessingBlocksTrackerInstance.ManualUnload(
                        PreprocessingBlockInstance
                    )
                    break
                # We found the root. This means that this preprocessing block is ready to start

                if ExecutedBlocksTrackerInstance.IsTracked(SearchBlockInstance):
                    continue
                # If the block has already been executed then we can skip it.

                if PreprocessingBlocksTrackerInstance.IsTracked(SearchBlockInstance):
                    break
                # There is a preceeding block that needs to be preprocessed. So we will skip this block for now
                # NOTE NOTE NOTE NOTE TODO There is a question if we need to only pay attention to blocks of same type or not. I say not for now

                if type(SearchBlockInstance).__name__ == MergePlates.__name__:
                    break
                # We can not start a preprocessing device if an unexecuted merge plates step preceeds it.
            # We are going to walk backward until we find either a merge plates step, a preceeding preprocessing device, or the beginning of the method

        for ConfirmedPreprocessingBlockInstance in ConfirmedPreprocessingBlockInstances:
            pass
            # I need to do something here for the preprocessing
        # Before each round of steps we want to check if we can start heaters / Coolers or other preprocessing devices
        # We can not start a preprocessing device until any preceeding merge steps are completed

        if InactiveContextTrackerInstance.IsTracked(
            WorkbookInstance.GetExecutingContext()
        ):
            if (
                ListInList(
                    ContextTrackerInstance.GetObjectsAsList(),
                    InactiveContextTrackerInstance.GetObjectsAsList(),
                )
                is True
            ):
                pass
            # If all contexts are inactive then we need to wait on devices to complete. TODO

            for ContextInstance in ContextTrackerInstance.GetObjectsAsList():
                if not InactiveContextTrackerInstance.IsTracked(
                    WorkbookInstance.GetExecutingContext()
                ):
                    WorkbookInstance.SetExecutingContext(ContextInstance)
                    break
            # find the context here

            ReversedExecutedBlocks: list[
                Block
            ] = ExecutedBlocksTrackerInstance.GetObjectsAsList().reverse()

            for BlockInstance in ReversedExecutedBlocks:
                if BlockInstance.GetContext() == WorkbookInstance.GetExecutingContext():
                    CurrentExecutingBlock: Block = BlockInstance
                    break
            # Set the tree current node here
        # Find the context we need to process if the current context is exhausted

        CurrentExecutingBlock = CurrentExecutingBlock.GetChildren()[0]
        # This should always be a single child. Only a split plate wil have 2 children
        # The two children will be executed in the split plate block

        if (
            sum(
                WellFactor.GetFactor()
                for WellFactor in WorkbookInstance.GetExecutingContext()
                .GetWellFactorTracker()
                .GetObjectsAsList()
            )
            != 0  # If all the factors are zero then technically the pathway is "dead" so it will never execute
            or type(CurrentExecutingBlock).__name__ == MergePlates.__name__
        ):
            # We will only execute the step if the factors are not zero
            # Additionally we must always execute a merge plates step no matter what

            CurrentExecutingBlock.Process(WorkbookInstance, HalInstance)
        ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
        # We must track all executed blocks even if processing is skipped.
        # A skipped block is still executed in the mind of the program


def WorkbookInit(WorkbookInstance: Workbook):

    # Check runtype. We will determine the starting well here
    if WorkbookInstance.GetRunType() == WorkbookRunTypes.Run:
        WorkbookInstance.StartingWell = None  # I made it none right now for testing
    else:
        WorkbookInstance.StartingWell = 1

    # Set Initial Active Context
    AspirateWellSequencesTrackerInstance = WellSequencesTracker()
    DispenseWellSequencesTrackerInstance = WellSequencesTracker()

    WellFactorsTrackerInstance = WellFactorTracker()

    for SampleNumber in range(0, WorkbookInstance.GetWorklist().GetNumSamples()):
        WellNumber = SampleNumber

        WellSequencesInstance = WellSequences(WellNumber, [WellNumber])
        WellFactorInstance = WellFactor(WellNumber, 1)

        AspirateWellSequencesTrackerInstance.ManualLoad(WellSequencesInstance)
        DispenseWellSequencesTrackerInstance.ManualLoad(WellSequencesInstance)

        WellFactorsTrackerInstance.ManualLoad(WellFactorInstance)

    WorkbookInstance.SetExecutingContext(
        Context(
            ":__StartingContext__",
            AspirateWellSequencesTrackerInstance,
            DispenseWellSequencesTrackerInstance,
            WellFactorsTrackerInstance,
        )
    )

    WorkbookInstance.GetContextTracker().ManualLoad(
        WorkbookInstance.GetExecutingContext()
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
