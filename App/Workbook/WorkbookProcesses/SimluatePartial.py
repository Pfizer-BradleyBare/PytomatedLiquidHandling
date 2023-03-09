import threading

from PytomatedLiquidHandling.API.Tools.LabwareSelection import LabwareSelectionLoader
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ...Workbook import Block, Workbook, WorkbookProcesses
from . import WorkbookFunctions


def SimulatePartial(WorkbookInstance: Workbook):
    from ...Handler import GetHandler

    WorkbookInstance.ExcelInstance.OpenBook(False)

    WorkbookFunctions.Initialize(WorkbookInstance)

    CurrentExecutingBlock: Block = WorkbookInstance.MethodTreeRoot
    CurrentExecutingBlock.Process(WorkbookInstance)
    WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
    # Do the first step processing here. First step is always a plate step.

    while True:

        if WorkbookFunctions.AllBlocksExecuted(WorkbookInstance):

            WorkbookInstance.LabwareSelectionTrackerInstance = (
                LabwareSelectionLoader.Load(WorkbookInstance.ContainerTrackerInstance)
            )

            # This is init and starting of the first thread. There are two threads that need to execute before the "system" is ready.
            # This second thread does a simulated run to confirm the method is "correct"

            WorkbookInstance.ExcelInstance.CloseBook()

            WorkbookInstance.APIRunType = RunTypes.SimulateFull

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

            GetHandler().GetLogger().info("Starting Simulate Full")

            WorkbookInstance.WorkbookProcessorThread.start()

            return
        # First thing to do is check if all blocks have been executed.

        # if AliveStateFlag.AliveStateFlag is False: TODO
        # Do some workbook save state stuff here
        #    return
        # The processing lock is used as a pause button to control which workbook executes.
        # During acquire we wait for the thread to be unpaused.
        # We immediately release so we do not stall the main process
        # After release we must check that the server still wants to execute. If not, we do some save state stuff then kill the thread.

        CurrentExecutingBlock = WorkbookFunctions.GetNextBlock(WorkbookInstance)
        # Find the context we need to process if the current context is exhausted

        WorkbookFunctions.ExecuteBlock(WorkbookInstance, CurrentExecutingBlock)
