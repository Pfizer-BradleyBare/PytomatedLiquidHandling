import os
import threading

from PytomatedLiquidHandling.API.Tools.Container.BaseContainer import ContainerTracker
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes
from PytomatedLiquidHandling.Tools.AbstractClasses import ObjectABC

from ..Tools.Context import Context, ContextTracker
from ..Tools.Excel import Excel
from ..Workbook import Block, BlockTracker, Worklist
from .WorkbookFunctions import Initialize

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
        RunType: RunTypes,
        MethodPath: str,
        MethodBlocksTrackerInstance: BlockTracker,
        WorklistInstance: Worklist,
        ExcelInstance: Excel,
    ):
        from ..Handler import GetHandler

        # Normal Init Variables
        # Variables
        self.RunType: RunTypes = RunType
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.MethodTreeRoot: Block = MethodBlocksTrackerInstance.GetObjectsAsList()[0]

        # Trackers
        self.MethodBlocksTrackerInstance: BlockTracker = MethodBlocksTrackerInstance
        self.WorklistInstance: Worklist = WorklistInstance
        self.ExcelInstance: Excel = ExcelInstance
        self.PreprocessingBlocksTrackerInstance: BlockTracker = BlockTracker()

        # Thread
        self.ProcessingLock: threading.Lock = threading.Lock()

        # Special Init Variables (These variables are allow to be set in the Workbook Init function to faciliate resets)

        # Variables
        self.ExecutingContextInstance: Context
        self.Simulate: bool

        # Trackers
        self.ExecutedBlocksTrackerInstance: BlockTracker
        self.ContainerTrackerInstance: ContainerTracker
        self.CompletedPreprocessingBlocksTrackerInstance: BlockTracker
        self.ContextTrackerInstance: ContextTracker
        self.ContextTrackerInstance: ContextTracker
        self.InactiveContextTrackerInstance: ContextTracker

        # Thread
        self.WorkbookProcessorThread: threading.Thread

        GetHandler().GetLogger().debug(
            "The following method tree was determined for %s: \n%s",
            self.MethodName,
            self.MethodTreeRoot,
        )

        # Do the necessary init function.
        # Why do it here? Because all init is handled inside the init function for simplicity sake

        Initialize(self)

    def GetName(self) -> str:
        return self.MethodName

    def GetPath(self) -> str:
        return self.MethodPath

    def GetRunType(self) -> RunTypes:
        return self.RunType

    def SetRunType(self, RunType: RunTypes):
        self.RunType = RunType

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

    def GetContextTracker(self) -> ContextTracker:
        return self.ContextTrackerInstance

    def GetInactiveContextTracker(self) -> ContextTracker:
        return self.InactiveContextTrackerInstance

    def GetExecutingContext(self) -> Context:
        return self.ExecutingContextInstance

    def SetExecutingContext(self, ContextInstance: Context) -> None:
        self.ExecutingContextInstance = ContextInstance

    def GetWorkbookProcessorThread(self) -> threading.Thread:
        return self.WorkbookProcessorThread

    def GetProcessingLock(self) -> threading.Lock:
        return self.ProcessingLock
