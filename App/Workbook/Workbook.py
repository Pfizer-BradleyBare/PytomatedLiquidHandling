import os
import threading

from PytomatedLiquidHandling.API.Tools.Container.BaseContainer import ContainerTracker
from PytomatedLiquidHandling.API.Tools.LabwareSelection import LabwareSelectionTracker
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes
from PytomatedLiquidHandling.Tools.AbstractClasses import ObjectABC

from ..Tools.Context import Context, ContextTracker
from ..Tools.Excel import Excel
from ..Workbook import Block, BlockTracker, Worklist
from . import WorkbookProcesses, WorkbookRunTypes

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
#
# NOTE: THIS EXPLANATION IS OUTDATED


class Workbook(ObjectABC):
    def __init__(
        self,
        WorkbookRunType: WorkbookRunTypes,
        MethodPath: str,
        MethodBlocksTrackerInstance: BlockTracker,
        WorklistInstance: Worklist,
        ExcelInstance: Excel,
    ):
        from ..Handler import GetHandler

        # Normal Init Variables
        # Variables
        self.WorkbookRunType: WorkbookRunTypes = WorkbookRunType
        self.APIRunType: RunTypes
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.MethodTreeRoot: Block = MethodBlocksTrackerInstance.GetObjectsAsList()[0]

        # Trackers
        self.MethodBlocksTrackerInstance: BlockTracker = MethodBlocksTrackerInstance
        self.WorklistInstance: Worklist = WorklistInstance
        self.ExcelInstance: Excel = ExcelInstance
        self.PreprocessingBlocksTrackerInstance: BlockTracker = BlockTracker()
        self.LabwareSelectionTrackerInstance: LabwareSelectionTracker

        # Thread
        self.ProcessingLock: threading.Lock = threading.Lock()

        # Special Init Variables (These variables are allow to be set in the Workbook Init function to faciliate resets)

        # Variables
        self.ExecutingContextInstance: Context

        # Trackers
        self.ExecutedBlocksTrackerInstance: BlockTracker
        self.ContainerTrackerInstance: ContainerTracker
        self.ExecutedPreprocessingBlocksTrackerInstance: BlockTracker
        self.ContextTrackerInstance: ContextTracker  # This is all the contexts
        self.InactiveContextTrackerInstance: ContextTracker  # This is only the inactive ones

        # Thread
        self.WorkbookProcessorThread: threading.Thread

        self.WorkbookProcessorThread = threading.Thread(
            name=self.GetName() + "-> Startup Process",
            target=WorkbookProcesses.StartupProcess,
            args=(self,),  # args must be tuple hence the empty second argument
        )

        self.WorkbookProcessorThread.start()

    def GetName(self) -> str:
        return self.MethodName

    def SetExecutingContext(self, ContextInstance: Context) -> None:
        self.ExecutingContextInstance = ContextInstance
