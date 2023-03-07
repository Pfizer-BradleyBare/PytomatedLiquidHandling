import os
import threading

from PytomatedLiquidHandling.API.Tools.Container.BaseContainer import ContainerTracker
from PytomatedLiquidHandling.API.Tools.LabwareSelection import LabwareSelectionTracker
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes
from PytomatedLiquidHandling.Tools.AbstractClasses import ObjectABC

from ..Tools.Context import Context, ContextTracker
from ..Tools.Excel import Excel
from ..Workbook import Block, BlockTracker, Worklist
from . import WorkbookFunctions, WorkbookRunTypes

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
        self.CompletedPreprocessingBlocksTrackerInstance: BlockTracker
        self.ContextTrackerInstance: ContextTracker
        self.ContextTrackerInstance: ContextTracker
        self.InactiveContextTrackerInstance: ContextTracker

        # Thread
        self.WorkbookProcessorThread: threading.Thread

        GetHandler().GetLogger().debug(
            "The following method tree was determined for %s: \n%s",
            self.MethodName,
            self.MethodTreeRoot.PrintBlockTree(),
        )

        # This is init and starting of the first thread. There are two threads that need to execute before the "system" is ready.
        # This first thread does a plate volume calculation then selects possible containers. We need this info before we can do a "full" run.
        WorkbookFunctions.Initialize(self)

        self.APIRunType = RunTypes.SimulatePartial

        self.WorkbookProcessorThread = threading.Thread(
            name=self.GetName()
            + "->"
            + self.WorkbookRunType.value
            + " : "
            + self.APIRunType,
            target=WorkbookFunctions.ProcessorSimulatePartial,
            args=(self,),  # args must be tuple hence the empty second argument
        )

        self.WorkbookProcessorThread.start()

    def GetName(self) -> str:
        return self.MethodName

    def SetExecutingContext(self, ContextInstance: Context) -> None:
        self.ExecutingContextInstance = ContextInstance
