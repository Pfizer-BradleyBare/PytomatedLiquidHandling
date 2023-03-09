from ....Blocks import Finish, MergePlates, Plate, SplitPlate
from ... import Block, Workbook


def IsDeadBlock(WorkbookInstance: Workbook, BlockInstance: Block) -> bool:
    from ....Handler import GetHandler

    if (
        isinstance(BlockInstance, Plate)
        or isinstance(BlockInstance, SplitPlate)
        or isinstance(BlockInstance, MergePlates)
        or isinstance(BlockInstance, Finish)
    ):
        return False
    # Pathway control blocks are never dead. They CRITICAL to correct flow of the program

    if (
        sum(
            WellFactor.GetFactor()
            for WellFactor in WorkbookInstance.ContextTrackerInstance.GetObjectByName(
                BlockInstance.GetContext()
            )
            .GetWellFactorTracker()
            .GetObjectsAsList()
        )
        != 0  # If all the factors are zero then technically the pathway is "dead" so it will never execute
    ):
        # We will only execute the step if the factors are not zero

        return False

    return True
