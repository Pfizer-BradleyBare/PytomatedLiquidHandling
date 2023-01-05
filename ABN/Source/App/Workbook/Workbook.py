import os
import threading
from enum import Enum

from ...API.Tools.Container.BaseContainer import ContainerTracker
from ...API.Tools.LabwareSelection import (
    LabwareSelectionLoader,
    LabwareSelectionTracker,
)
from ...Server.Globals import LOG  # , AliveStateFlag
from ...Tools.AbstractClasses import ObjectABC
from ..Blocks import MergePlates
from ..Tools.Container import Plate
from ..Tools.Context import (
    Context,
    ContextTracker,
    WellFactor,
    WellFactorTracker,
    WellSequence,
    WellSequenceTracker,
)
from ..Tools.Timer import TimerTracker
from .Block import Block, BlockTracker
from .Worklist import Worklist


class WorkbookStates(Enum):
    def __init__(self, a, b):
        self.State = a
        self.Reason = b

    Queued = (
        "Queued",
        "Method is ready for deck loading but space is not available or method is not next in queue.",
    )

    Running = (
        "Running",
        "Method is running normally. No interaction from the user is required.",
    )

    WaitingPaused = (
        "Waiting: Paused",
        "User paused this method manually. Method will not proceed until unpaused.",
    )

    WaitingDeckLoading = (
        "Waiting: Deck Loading",
        "The method is ready to run but the deck must be loaded first. Please proceed to load the deck.",
    )

    WaitingTimer = (
        "Waiting: Timer",
        "The method is running correctly but no contexts are active. Most likely waiting on a timer of some sort.",
    )

    WaitingNotification = (
        "Waiting: Notification",
        "A notification was fired that waits on the user before proceeding. Please confirm the notification to continue.",
    )

    WaitingError = (
        "Waiting: Error",
        "An error occured. Please correct.",  # TODO
    )

    Aborted = (
        "Aborted",
        "User has aborted this method manually. Only deck unloading is allowed.",
    )
    # The user stopped the method but it is still in the list. This allows the user to remove plates and all that jazz

    Complete = (
        "Complete",
        "Method execution is complete. Only deck unloading is allowed.",
    )
    # The user stopped the method but it is still in the list. This allows the user to remove plates and all that jazz

    Dequeued = (
        "Dequeued",
        "Method no longer 'exists' in the system. This is here for book keeping only. User will never see this state.",
    )
    # The user stopped the method but it is still in the list. This allows the user to remove plates and all that jazz


class WorkbookRunTypes(Enum):
    Test = "Test"  # This is a single programmatic test to check method is compatible with system
    Prep = "Prep"  # This will test with all samples added then generate a preparation list for the user
    Run = "Run"  # This will queue to run on the system
    PreRun = "PreRun"


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
    ):

        # Normal Init Variables

        # Variables
        self.RunType: WorkbookRunTypes = RunType
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.State: WorkbookStates = WorkbookStates.Queued
        self.MethodTreeRoot: Block = MethodBlocksTrackerInstance.GetObjectsAsList()[0]

        # Trackers
        self.MethodBlocksTrackerInstance: BlockTracker = MethodBlocksTrackerInstance
        self.WorklistInstance: Worklist = WorklistInstance
        self.LabwareSelectionTrackerInstance = LabwareSelectionTracker()

        # Thread
        self.ProcessingLock: threading.Lock = threading.Lock()

        # Special Init Variables (These variables are allow to be set in the Workbook Init function to faciliate resets)

        # Variables
        self.ExecutingContextInstance: Context

        # Trackers
        self.ExecutedBlocksTrackerInstance: BlockTracker
        self.ContainerTrackerInstance: ContainerTracker
        self.PreprocessingBlocksTrackerInstance: BlockTracker = BlockTracker()
        self.ActiveContextTrackerInstance: ContextTracker
        self.InactiveContextTrackerInstance: ContextTracker
        self.TimerTrackerInstance: TimerTracker

        # Thread
        self.WorkbookProcessorThread: threading.Thread

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

    def SetRunType(self, RunType: WorkbookRunTypes):
        self.RunType = RunType

    def GetState(self) -> WorkbookStates:
        return self.State

    def SetState(self, State: WorkbookStates):
        self.State = State

    def GetMethodTreeRoot(self) -> Block:
        return self.MethodTreeRoot

    def GetMethodBlocksTracker(self) -> BlockTracker:
        return self.MethodBlocksTrackerInstance

    def GetExecutedBlocksTracker(self) -> BlockTracker:
        return self.ExecutedBlocksTrackerInstance

    def GetPreprocessingBlocksTracker(self) -> BlockTracker:
        return self.PreprocessingBlocksTrackerInstance

    def GetWorklist(self) -> Worklist:
        return self.WorklistInstance

    def GetContainerTracker(self) -> ContainerTracker:
        return self.ContainerTrackerInstance

    def GetActiveContextTracker(self) -> ContextTracker:
        return self.ActiveContextTrackerInstance

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

    ActiveContextTrackerInstance = WorkbookInstance.GetActiveContextTracker()
    InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()
    ExecutedBlocksTrackerInstance = WorkbookInstance.GetExecutedBlocksTracker()
    PreprocessingBlocksTrackerInstance = (
        WorkbookInstance.GetPreprocessingBlocksTracker()
    )

    CurrentExecutingBlock: Block = WorkbookInstance.GetMethodTreeRoot()
    CurrentExecutingBlock.Process(WorkbookInstance)
    ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
    # Do the first step processing here. First step is always a plate step.

    while True:

        WorkbookInstance.SetState(WorkbookStates.WaitingDeckLoading)

        while True:
            WorkbookInstance.ProcessingLock.acquire()
            WorkbookInstance.ProcessingLock.release()
            # if AliveStateFlag.AliveStateFlag is False: TODO
            # Do some workbook save state stuff here
            #    return

            # if all(
            #    LoadedLabwareConnection.IsConnected()
            #    for LoadedLabwareConnection in WorkbookInstance.GetLoadedLabwareConnectionTracker().GetObjectsAsList()
            # ):
            break
            # if all are connected then we can start running. Boom!
        # This first thing we need to do is check that all labwares are loaded. If not then we sit here and wait.
        # This could be expanded to wait until a set of labware is loaded before proceeding. How? No idea.

        WorkbookInstance.SetState(WorkbookStates.Running)

        if all(
            item in ExecutedBlocksTrackerInstance.GetObjectsAsList()
            for item in WorkbookInstance.GetMethodBlocksTracker().GetObjectsAsList()
        ):

            print("HERE")

            WorkbookInstance.LabwareSelectionTrackerInstance = (
                LabwareSelectionLoader.Load(
                    WorkbookInstance.GetContainerTracker(),
                )
            )

            for (
                LabwareSelectionInstance
            ) in WorkbookInstance.LabwareSelectionTrackerInstance.GetObjectsAsList():
                print(LabwareSelectionInstance.GetName())

            if WorkbookInstance.GetRunType() == WorkbookRunTypes.PreRun:

                WorkbookInstance.SetRunType(WorkbookRunTypes.Run)
                WorkbookInstance.SetState(WorkbookStates.Queued)

                WorkbookInstance.ProcessingLock.acquire()
                WorkbookInstance.ProcessingLock.release()
                # if AliveStateFlag.AliveStateFlag is False: TODO
                # Do some workbook save state stuff here
                #    return
                # Everything is controlled by the server. So we will wait here for the server to tell us we are next to run
                # Then we will reinit the workbook and wait on deck loading

                WorkbookInit(WorkbookInstance)
            # If we are prerun then we need to do this another time to actually run the method
            # else we are done here and can return

            return
        # First thing to do is check if all blocks have been executed.

        WorkbookInstance.ProcessingLock.acquire()
        WorkbookInstance.ProcessingLock.release()
        # if AliveStateFlag.AliveStateFlag is False: TODO
        # Do some workbook save state stuff here
        #    return
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
                    break
                # We found the root. This means that this preprocessing block is ready to start

                if ExecutedBlocksTrackerInstance.IsTracked(
                    SearchBlockInstance.GetName()
                ):
                    continue
                # If the block has already been executed then we can skip it.

                if PreprocessingBlocksTrackerInstance.IsTracked(
                    SearchBlockInstance.GetName()
                ):
                    break
                # There is a preceeding block that needs to be preprocessed. So we will skip this block for now
                # NOTE NOTE NOTE NOTE TODO There is a question if we need to only pay attention to blocks of same type or not. I say not for now

                if type(SearchBlockInstance).__name__ == MergePlates.__name__:
                    break
                # We can not start a preprocessing device if an unexecuted merge plates step preceeds it.
            # We are going to walk backward until we find either a merge plates step, a preceeding preprocessing device, or the beginning of the method

        for ConfirmedPreprocessingBlockInstance in ConfirmedPreprocessingBlockInstances:
            ConfirmedPreprocessingBlockInstance.Preprocess(WorkbookInstance)
        # Before each round of steps we want to check if we can start heaters / Coolers or other preprocessing devices
        # We can not start a preprocessing device until any preceeding merge steps are completed

        if InactiveContextTrackerInstance.IsTracked(
            WorkbookInstance.GetExecutingContext().GetName()
        ):
            if all(
                item in InactiveContextTrackerInstance.GetObjectsAsList()
                for item in ActiveContextTrackerInstance.GetObjectsAsList()
            ):
                WorkbookInstance.SetState(WorkbookStates.WaitingTimer)
            # If all contexts are inactive then we need to wait on devices to complete. TODO

            for ContextInstance in ActiveContextTrackerInstance.GetObjectsAsList():
                if not InactiveContextTrackerInstance.IsTracked(
                    WorkbookInstance.GetExecutingContext().GetName()
                ):
                    WorkbookInstance.SetExecutingContext(ContextInstance)
                    break
            # find the context here

            ReversedExecutedBlocks: list[
                Block
            ] = ExecutedBlocksTrackerInstance.GetObjectsAsList()
            ReversedExecutedBlocks.reverse()

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

            print("EXECUTING", CurrentExecutingBlock.GetName())
            CurrentExecutingBlock.Process(WorkbookInstance)
        ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
        # We must track all executed blocks even if processing is skipped.
        # A skipped block is still executed in the mind of the program


def WorkbookInit(WorkbookInstance: Workbook):

    # Setup special varibles

    # Trackers
    WorkbookInstance.ExecutedBlocksTrackerInstance = BlockTracker()
    WorkbookInstance.ContainerTrackerInstance = ContainerTracker()
    WorkbookInstance.ActiveContextTrackerInstance = ContextTracker()
    WorkbookInstance.InactiveContextTrackerInstance = ContextTracker()
    WorkbookInstance.TimerTrackerInstance = TimerTracker()

    # Thread
    WorkbookInstance.WorkbookProcessorThread = threading.Thread(
        name=WorkbookInstance.GetName() + "->" + WorkbookInstance.GetRunType().value,
        target=WorkbookProcessor,
        args=(WorkbookInstance,),  # args must be tuple hence the empty second argument
    )

    # Set Initial Active Context
    AspirateWellSequenceTrackerInstance = WellSequenceTracker()
    DispenseWellSequenceTrackerInstance = WellSequenceTracker()

    WellFactorsTrackerInstance = WellFactorTracker()

    for SampleNumber in range(1, WorkbookInstance.GetWorklist().GetNumSamples() + 1):
        WellNumber = SampleNumber

        WellSequencesInstance = WellSequence(WellNumber, WellNumber)
        WellFactorInstance = WellFactor(WellNumber, 1)

        AspirateWellSequenceTrackerInstance.ManualLoad(WellSequencesInstance)
        DispenseWellSequenceTrackerInstance.ManualLoad(WellSequencesInstance)

        WellFactorsTrackerInstance.ManualLoad(WellFactorInstance)

    WorkbookInstance.SetExecutingContext(
        Context(
            ":__StartingContext__",
            AspirateWellSequenceTrackerInstance,
            DispenseWellSequenceTrackerInstance,
            WellFactorsTrackerInstance,
        )
    )

    WorkbookInstance.GetActiveContextTracker().ManualLoad(
        WorkbookInstance.GetExecutingContext()
    )

    WorkbookInstance.GetContainerTracker().PlateTrackerInstance.ManualLoad(
        Plate(
            "__StartingContext__", WorkbookInstance.GetName(), "No Preference"
        )  # This will never be loaded so filter doesn't matter
    )
    # Setting initial context and container.
    if WorkbookInstance.GetRunType() == WorkbookRunTypes.Run:
        pass
        # WorkbookInstance.ProcessingLock.acquire()

    WorkbookInstance.WorkbookProcessorThread.start()
