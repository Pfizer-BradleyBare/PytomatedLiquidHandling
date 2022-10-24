from .WorkbookTracker import WorkbookTracker
from .Workbook import Workbook, WorkbookRunTypes
from ...Tools import Excel, Tree
from .Worklist import Worklist
from .Solution import SolutionTracker, SolutionLoader
from .Block import BlockLoader, BlockTracker
from ...HAL.Tools import DeckLoadingItemTracker


def Load(
    WorkbookTrackerInstance: WorkbookTracker,
    ExcelFilePath: str,
    RunType: WorkbookRunTypes,
):
    ExcelInstance = Excel(ExcelFilePath)

    WorklistInstance = Worklist(ExcelInstance)
    SolutionTrackerInstance = SolutionTracker()

    SolutionLoader.Load(SolutionTrackerInstance, ExcelInstance)

    BlockTrackerInstance = BlockTracker()
    BlockLoader.Load(BlockTrackerInstance, ExcelInstance)

    TreeInstance = Tree(BlockTrackerInstance.GetObjectsAsList()[0])

    WorkbookTrackerInstance.ManualLoad(
        Workbook(
            RunType,
            ExcelFilePath,
            TreeInstance,
            WorklistInstance,
            SolutionTrackerInstance,
            None,  # There will never be a deck loading unless we resume a run. But we havn't gotten there yet...
        )
    )
