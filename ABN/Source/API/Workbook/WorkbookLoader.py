from .WorkbookTracker import WorkbookTracker
from .Workbook import Workbook, WorkbookRunTypes
from ...Tools import Excel, Tree
from .Worklist import Worklist
from .Solution import SolutionTracker, SolutionLoader
from .Block import BlockLoader, BlockTracker


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

    WorkbookTrackerInstance.LoadManual(
        Workbook(
            RunType,
            ExcelFilePath,
            TreeInstance,
            WorklistInstance,
            SolutionTrackerInstance,
        )
    )
