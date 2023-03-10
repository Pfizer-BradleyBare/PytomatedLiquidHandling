import threading

from PytomatedLiquidHandling.API.Tools.LabwareSelection import LabwareSelectionLoader
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ...Workbook import Workbook, WorkbookProcesses
from . import WorkbookFunctions


def SimulatePartial(WorkbookInstance: Workbook):
    from ...Handler import GetHandler

    GetHandler().GetLogger().info("Starting Simulate Partial")

    WorkbookInstance.APIRunType = RunTypes.SimulatePartial

    WorkbookInstance.ExcelInstance.OpenBook(False)

    WorkbookFunctions.Initialize(WorkbookInstance)

    WorkbookFunctions.DoFirstBlockProcessing(WorkbookInstance)

    while True:

        if WorkbookFunctions.AllBlocksExecuted(WorkbookInstance):

            WorkbookInstance.LabwareSelectionTrackerInstance = (
                LabwareSelectionLoader.Load(WorkbookInstance.ContainerTrackerInstance)
            )
            # This is init and starting of the first thread. There are two threads that need to execute before the "system" is ready.
            # This second thread does a simulated run to confirm the method is "correct"

            WorkbookInstance.ExcelInstance.CloseBook()

            WorkbookInstance.WorkbookProcessorThread = threading.Thread(
                name=WorkbookInstance.GetName()
                + "->"
                + WorkbookInstance.WorkbookRunType.value
                + " : "
                + WorkbookInstance.APIRunType.value,
                target=WorkbookProcesses.SimulateFull,
                args=(
                    WorkbookInstance,
                ),  # args must be tuple hence the empty second argument
            )

            WorkbookInstance.WorkbookProcessorThread.start()

            return
            # First thing to do is check if all blocks have been executed.

        if not GetHandler().IsAlive():
            return

        CurrentExecutingBlock = WorkbookFunctions.GetNextBlock(WorkbookInstance)
        # Find the context we need to process if the current context is exhausted

        WorkbookFunctions.HandleBlockExecution(
            WorkbookInstance,
            CurrentExecutingBlock,
            WorkbookInstance.ExecutedBlocksTrackerInstance,
            "Process",
        )
