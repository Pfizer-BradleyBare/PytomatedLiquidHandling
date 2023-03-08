import threading

from PytomatedLiquidHandling.API.Tools.LabwareSelection import LabwareSelectionLoader
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ...Blocks import MergePlates
from ...Workbook import Block, Workbook, WorkbookFunctions


def ProcessorSimulatePartial(WorkbookInstance: Workbook):
    from ...Handler import GetHandler

    WorkbookInstance.ExcelInstance.OpenBook(False)

    ContextTrackerInstance = WorkbookInstance.ContextTrackerInstance
    InactiveContextTrackerInstance = WorkbookInstance.InactiveContextTrackerInstance
    ExecutedBlocksTrackerInstance = WorkbookInstance.ExecutedBlocksTrackerInstance

    CurrentExecutingBlock: Block = WorkbookInstance.MethodTreeRoot
    CurrentExecutingBlock.Process(WorkbookInstance)
    ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
    # Do the first step processing here. First step is always a plate step.

    while True:

        if all(
            item in ExecutedBlocksTrackerInstance.GetObjectsAsList()
            for item in WorkbookInstance.MethodBlocksTrackerInstance.GetObjectsAsList()
        ):

            WorkbookInstance.LabwareSelectionTrackerInstance = (
                LabwareSelectionLoader.Load(WorkbookInstance.ContainerTrackerInstance)
            )

            # This is init and starting of the first thread. There are two threads that need to execute before the "system" is ready.
            # This second thread does a simulated run to confirm the method is "correct"
            WorkbookFunctions.Initialize(WorkbookInstance)

            WorkbookInstance.APIRunType = RunTypes.SimulateFull

            WorkbookInstance.WorkbookProcessorThread = threading.Thread(
                name=WorkbookInstance.GetName()
                + "->"
                + WorkbookInstance.WorkbookRunType.value
                + " : "
                + WorkbookInstance.APIRunType.value,
                target=WorkbookFunctions.ProcessorSimulateFull,
                args=(
                    WorkbookInstance,
                ),  # args must be tuple hence the empty second argument
            )

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

        if InactiveContextTrackerInstance.IsTracked(
            WorkbookInstance.ExecutingContextInstance.GetName()
        ):
            for ContextInstance in ContextTrackerInstance.GetObjectsAsList():
                if not InactiveContextTrackerInstance.IsTracked(
                    ContextInstance.GetName()
                ):
                    WorkbookInstance.SetExecutingContext(ContextInstance)
                    break
            # find the context here

            ReversedExecutedBlocks: list[
                Block
            ] = ExecutedBlocksTrackerInstance.GetObjectsAsList()
            ReversedExecutedBlocks.reverse()

            for BlockInstance in ReversedExecutedBlocks:
                if (
                    BlockInstance.GetContext()
                    == WorkbookInstance.ExecutingContextInstance
                ):
                    CurrentExecutingBlock: Block = BlockInstance
                    break
            # Set the tree current node here
        # Find the context we need to process if the current context is exhausted

        CurrentExecutingBlock = CurrentExecutingBlock.GetChildren()[0]

        if (
            sum(
                WellFactor.GetFactor()
                for WellFactor in WorkbookInstance.ExecutingContextInstance.GetWellFactorTracker().GetObjectsAsList()
            )
            != 0  # If all the factors are zero then technically the pathway is "dead" so it will never execute
            or type(CurrentExecutingBlock).__name__ == MergePlates.__name__
        ):
            # We will only execute the step if the factors are not zero
            # Additionally we must always execute a merge plates step no matter what

            GetHandler().GetLogger().info(
                "EXECUTING: " + CurrentExecutingBlock.GetName()
            )
            StepStatus = CurrentExecutingBlock.Process(WorkbookInstance)

        else:
            StepStatus = True
            GetHandler().GetLogger().info(
                "SKIPPING: " + CurrentExecutingBlock.GetName()
            )

        if StepStatus is True:
            ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)

            # need to fix with new stepstatus TODO
            # This should always be a single child. Only a split plate wil have 2 children
            # The two children will be executed in the split plate block
            # We must track all executed blocks even if processing is skipped.

        # NOTE: A skipped block is still executed in the mind of the program

        else:
            CurrentExecutingBlock = CurrentExecutingBlock.GetParentNode()  # type:ignore
