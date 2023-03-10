from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from .. import Workbook
from . import WorkbookFunctions


def Run(WorkbookInstance: Workbook):

    from ...Handler import GetHandler

    GetHandler().GetLogger().info("Starting Run")

    WorkbookInstance.APIRunType = RunTypes.Run

    WorkbookInstance.ExcelInstance.OpenBook(False)

    WorkbookFunctions.Initialize(WorkbookInstance)

    WorkbookFunctions.DoFirstBlockProcessing(WorkbookInstance)

    while True:

        if WorkbookFunctions.AllBlocksExecuted(WorkbookInstance):
            WorkbookInstance.ExcelInstance.CloseBook()
            return
        # First thing to do is check if all blocks have been executed.

        WorkbookInstance.ProcessingLock.acquire()
        WorkbookInstance.ProcessingLock.release()
        # if not GetHandler().IsAlive():
        # Do some workbook save state stuff here
        #    return
        # The processing lock is used as a pause button to control which workbook executes.
        # During acquire we wait for the thread to be unpaused.
        # We immediately release so we do not stall the main process
        # After release we must check that the server still wants to execute. If not, we do some save state stuff then kill the thread.

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
