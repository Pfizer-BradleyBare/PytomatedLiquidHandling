from ...Tools import Excel, ExcelHandle
from ..Tools.LoadedLabwareConnection import LoadedLabwareConnectionTracker
from .Block import BlockLoader, BlockTracker
from .Solution import SolutionLoader, SolutionTracker
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
        SolutionTrackerInstance = SolutionTracker()

        SolutionLoader.Load(SolutionTrackerInstance, ExcelInstance)

        BlockTrackerInstance = BlockTracker()
        BlockLoader.Load(BlockTrackerInstance, ExcelInstance)

        WorkbookTrackerInstance.ManualLoad(
            Workbook(
                RunType,
                ExcelFilePath,
                BlockTrackerInstance,
                WorklistInstance,
                SolutionTrackerInstance,
                LoadedLabwareConnectionTracker(),  # There will never be a deck loading unless we resume a run. But we havn't gotten there yet...
                BlockTracker(),
            )
        )
