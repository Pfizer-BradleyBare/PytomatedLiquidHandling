import threading

from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ...Workbook import Workbook, WorkbookProcesses
from . import WorkbookFunctions


def SimulateFull(WorkbookInstance: Workbook):

    from ...Handler import GetHandler

    GetHandler().GetLogger().info("Starting Simulate Full")

    WorkbookInstance.APIRunType = RunTypes.SimulateFull

    # We need to create some "Imaginary" plates to do the partial simulation. Should we do this for every combination? Is that practical?

    WorkbookInstance.ExcelInstance.OpenBook(False)

    WorkbookFunctions.Initialize(WorkbookInstance)

    WorkbookFunctions.DoFirstBlockProcessing(WorkbookInstance)

    while True:

        if WorkbookFunctions.AllBlocksExecuted(WorkbookInstance):
            WorkbookInstance.ExcelInstance.CloseBook()
            return
        # First thing to do is check if all blocks have been executed.

        if not GetHandler().IsAlive():
            return

        for BlockInstance in WorkbookFunctions.GetPreprocessingBlocks(
            WorkbookInstance
        ).GetObjectsAsList():
            WorkbookFunctions.HandleBlockExecution(
                WorkbookInstance,
                BlockInstance,
                WorkbookInstance.ExecutedPreprocessingBlocksTrackerInstance,
                "Preprocess",
            )

        CurrentExecutingBlock = WorkbookFunctions.GetNextBlock(WorkbookInstance)
        # Find the context we need to process if the current context is exhausted

        WorkbookFunctions.HandleBlockExecution(
            WorkbookInstance,
            CurrentExecutingBlock,
            WorkbookInstance.ExecutedBlocksTrackerInstance,
            "Process",
        )
    # We need to do the run. The run processor is what we want to simulate so we will just call that method

    # Now we need to wait for the user to load plates before doing the full run.
