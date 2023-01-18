from ..Tools.Excel import Excel, ExcelHandle
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
    with ExcelHandle(False) as ExcelHandleInstance:

        ExcelInstance = Excel(ExcelFilePath)
        ExcelInstance.AttachHandle(ExcelHandleInstance)

        WorklistInstance = Worklist(ExcelInstance)

        BlockTrackerInstance = BlockTracker()
        BlockLoader.Load(BlockTrackerInstance, ExcelInstance)

        WorkbookTrackerInstance.ManualLoad(
            Workbook(
                RunType,
                ExcelFilePath,
                BlockTrackerInstance,
                WorklistInstance,
                ExcelInstance,
            )
        )
