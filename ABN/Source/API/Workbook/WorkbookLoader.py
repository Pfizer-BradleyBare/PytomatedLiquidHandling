from .WorkbookTracker import WorkbookTracker
from .Workbook import Workbook
from ...Tools import Excel
from .Worklist import Worklist
from .Solution import SolutionTracker, SolutionLoader
from .Block import BlockLoader


def Load(WorkbookTrackerInstance: WorkbookTracker, ExcelFilePath: str):
    ExcelInstance = Excel(ExcelFilePath)

    WorklistInstance = Worklist(ExcelInstance)
    SolutionTrackerInstance = SolutionTracker(ExcelInstance)

    SolutionLoader.Load(SolutionTrackerInstance)

    BlockTrackerInstances = list()
    BlockLoader.Load(BlockTrackerInstances, ExcelInstance)

    WorkbookTrackerInstance.LoadManual(
        Workbook(
            ExcelFilePath,
            BlockTrackerInstances,
            WorklistInstance,
            SolutionTrackerInstance,
        )
    )
