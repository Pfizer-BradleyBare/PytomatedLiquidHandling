from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ..Tools.Excel import Excel
from ..Workbook import BlockTracker, Workbook, WorkbookTracker, Worklist
from .Block import BlockLoader


def Load(
    WorkbookTrackerInstance: WorkbookTracker,
    ExcelFilePath: str,
    RunType: RunTypes,
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
