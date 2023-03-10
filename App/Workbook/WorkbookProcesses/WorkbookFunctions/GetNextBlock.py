from ....Blocks import Plate
from ....Workbook import Block, Workbook
from .IsDeadBlock import IsDeadBlock


def GetNextBlock(WorkbookInstance: Workbook) -> Block:
    from ....Handler import GetHandler

    InactiveContextTrackerInstance = WorkbookInstance.InactiveContextTrackerInstance

    if InactiveContextTrackerInstance.IsTracked(
        WorkbookInstance.ExecutingContextInstance.GetName()
    ):
        for (
            ContextInstance
        ) in WorkbookInstance.ContextTrackerInstance.GetObjectsAsList():
            if not InactiveContextTrackerInstance.IsTracked(ContextInstance.GetName()):
                WorkbookInstance.SetExecutingContext(ContextInstance)
                break
        # find the context here

    ReversedExecutedBlocks: list[
        Block
    ] = WorkbookInstance.ExecutedBlocksTrackerInstance.GetObjectsAsList()
    ReversedExecutedBlocks.reverse()

    for BlockInstance in ReversedExecutedBlocks:
        if isinstance(BlockInstance, Plate):
            Context = (
                BlockInstance.GetContext()
                + ":"
                + BlockInstance.PlateName.Read(WorkbookInstance)
            )
        else:
            Context = BlockInstance.GetContext()

        if Context == WorkbookInstance.ExecutingContextInstance.GetName():
            LatestExecutedBlock: Block = BlockInstance

            NextBlock = LatestExecutedBlock.GetChildren()[0]

            if IsDeadBlock(WorkbookInstance, NextBlock):
                GetHandler().GetLogger().info(
                    "This block is not required for any samples. Skipping: "
                    + NextBlock.GetName()
                )
                WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(NextBlock)
                return GetNextBlock(WorkbookInstance)
            # skipping dead blocks

            return LatestExecutedBlock.GetChildren()[0]
        # Set the tree current node here
    # Find the context we need to process if the current context is exhausted

    raise Exception("This should never happen...")
