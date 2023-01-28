from ..Tools.Excel import Excel
from .Block import BlockLoader, BlockTracker
from .Solution import SolutionLoader
from .Workbook import Workbook, WorkbookRunTypes
from .WorkbookTracker import WorkbookTracker
from .Worklist import Worklist


def Load(
    WorkbookTrackerInstance: WorkbookTracker,
    ExcelFilePath: str,
    RunType: WorkbookRunTypes,
):

    ExcelInstance = Excel(ExcelFilePath)
    ExcelInstance.OpenBook(False)

    WorklistInstance = Worklist(ExcelInstance)

    BlockTrackerInstance = BlockTracker()
    BlockLoader.Load(BlockTrackerInstance, ExcelInstance)

    ExcelInstance.CloseBook()

    WorkbookTrackerInstance.ManualLoad(
        Workbook(
            RunType,
            ExcelFilePath,
            BlockTrackerInstance,
            WorklistInstance,
            ExcelInstance,
        )
    )
