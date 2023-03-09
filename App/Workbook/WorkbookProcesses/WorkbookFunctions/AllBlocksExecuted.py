from ... import Workbook


def AllBlocksExecuted(WorkbookInstance: Workbook) -> bool:
    ...

    if all(
        item in WorkbookInstance.ExecutedBlocksTrackerInstance.GetObjectsAsList()
        for item in WorkbookInstance.MethodBlocksTrackerInstance.GetObjectsAsList()
    ):
        return True

    return False
