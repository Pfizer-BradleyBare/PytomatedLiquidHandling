from typing import cast

from ....Blocks import Plate
from ....Workbook import Block, Workbook


def GetNextBlock(WorkbookInstance: Workbook) -> Block:
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
        print(BlockInstance.GetName())
        if isinstance(BlockInstance, Plate):
            Context = (
                BlockInstance.GetContext()
                + ":"
                + BlockInstance.PlateName.Read(WorkbookInstance)
            )
        else:
            Context = BlockInstance.GetContext()

        print(Context)
        print(WorkbookInstance.ExecutingContextInstance.GetName())

        if Context == WorkbookInstance.ExecutingContextInstance.GetName():
            print("HERE")
            LatestExecutedBlock: Block = BlockInstance
            return LatestExecutedBlock.GetChildren()[0]
        # Set the tree current node here
    # Find the context we need to process if the current context is exhausted

    raise Exception("This should never happen...")
