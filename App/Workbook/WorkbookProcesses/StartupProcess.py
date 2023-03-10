import threading

from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ...Workbook import Workbook, WorkbookProcesses


def StartupProcess(WorkbookInstance: Workbook):
    from ...Handler import GetHandler

    GetHandler().GetLogger().info("Starting Workbook Startup Process")

    GetHandler().GetLogger().info(
        "The following method tree was determined for %s: \n%s",
        WorkbookInstance.MethodName,
        WorkbookInstance.MethodTreeRoot.PrintBlockTree(),
    )

    WorkbookInstance.WorkbookProcessorThread = threading.Thread(
        name=WorkbookInstance.GetName() + "-> Startup Process",
        target=WorkbookProcesses.SimulatePartial,
        args=(WorkbookInstance,),  # args must be tuple hence the empty second argument
    )

    WorkbookInstance.ProcessingLock.acquire()

    WorkbookInstance.WorkbookProcessorThread.start()

    return
