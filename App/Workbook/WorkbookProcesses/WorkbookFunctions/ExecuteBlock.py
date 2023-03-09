from ....Blocks import MergePlates
from ....Workbook import Block, Workbook


def ExecuteBlock(WorkbookInstance: Workbook, BlockInstance: Block):
    from ....Handler import GetHandler

    if (
        sum(
            WellFactor.GetFactor()
            for WellFactor in WorkbookInstance.ExecutingContextInstance.GetWellFactorTracker().GetObjectsAsList()
        )
        != 0  # If all the factors are zero then technically the pathway is "dead" so it will never execute
        or type(BlockInstance).__name__ == MergePlates.__name__
    ):
        # We will only execute the step if the factors are not zero
        # Additionally we must always execute a merge plates step no matter what

        GetHandler().GetLogger().info("EXECUTING: " + BlockInstance.GetName())
        StepStatus = BlockInstance.Process(WorkbookInstance)

    else:
        StepStatus = True
        GetHandler().GetLogger().info("SKIPPING: " + BlockInstance.GetName())

    if StepStatus is True:
        WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(BlockInstance)
    # NOTE: A skipped block is still executed in the mind of the program
