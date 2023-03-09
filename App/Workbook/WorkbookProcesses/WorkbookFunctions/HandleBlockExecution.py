from typing import Callable

from ... import Block, BlockTracker, Workbook


def HandleBlockExecution(
    WorkbookInstance: Workbook,
    BlockInstance: Block,
    BlockTrackerInstance: BlockTracker,
    BlockFunction: str,
):
    from ....Handler import GetHandler

    GetHandler().GetLogger().info(
        "Executing " + BlockFunction + ": " + BlockInstance.GetName()
    )
    StepStatus = BlockInstance.__getattribute__(BlockFunction)(WorkbookInstance)

    if StepStatus is True:
        BlockTrackerInstance.ManualLoad(BlockInstance)
