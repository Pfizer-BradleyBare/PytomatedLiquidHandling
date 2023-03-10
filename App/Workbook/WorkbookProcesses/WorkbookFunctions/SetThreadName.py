import threading

from ....Workbook import Workbook


def SetThreadName(WorkbookInstance: Workbook):
    from ....Handler import GetHandler

    GetHandler().GetLogger().info(
        "Starting "
        + WorkbookInstance.GetName()
        + " -> "
        + WorkbookInstance.WorkbookRunType.value
        + " : "
        + WorkbookInstance.APIRunType.value
    )

    threading.current_thread().name = (
        WorkbookInstance.GetName()
        + "->"
        + WorkbookInstance.WorkbookRunType.value
        + " : "
        + WorkbookInstance.APIRunType.value
    )
