from .Block import BlockObjectCreationWrapper
from .BlockTracker import BlockTracker
from ....Tools import Excel
from ...Blocks import *  # noqa F403


def Load(BlockTrackerInstances: list[BlockTracker], ExcelInstance: Excel):
    MethodSheet = ExcelInstance.ReadMethodSheet()

    Rows = len(MethodSheet)
    Cols = len(MethodSheet[0])

    BlockInstances = list()
    BlockColumnNumbers = list()

    for RowIndex in range(0, Rows):
        for ColIndex in range(0, Cols):
            Name: str = MethodSheet[RowIndex][ColIndex]

            if Name is None:
                continue

            if type(Name) is not str:
                continue

            if " - (Click Here to Update)" not in Name:
                continue

            Name = Name.replace(" - (Click Here to Update)", "")

            BlockInstances.append(
                BlockObjectCreationWrapper(
                    ExcelInstance, Name, RowIndex + 1, ColIndex + 1
                )
            )
            BlockColumnNumbers.append(ColIndex)
    # Put blocks in a list sorted by row

    FinalList = list()

    def TracePathways(
        List,
        Instances: list[Block],
        StartingCol,
        StartingDifference,
        DifferenceChange,
    ):

        while len(Instances) != 0:
            Instance = Instances.pop(0)

            if Instance.GetCol() == StartingCol:
                List.append(Instance)

            elif Instance.GetCol() == StartingCol - StartingDifference:
                NewList = List + [Instance]
                TracePathways(
                    NewList,
                    Instances,
                    StartingCol - StartingDifference,
                    StartingDifference - DifferenceChange,
                    DifferenceChange,
                )

            elif Instance.GetCol() == StartingCol + StartingDifference:
                NewList = List + [Instance]
                TracePathways(
                    NewList,
                    Instances,
                    StartingCol + StartingDifference,
                    StartingDifference - DifferenceChange,
                    DifferenceChange,
                )

            else:
                Instances.append(Instance)

            if Instance.GetCol() == -1:
                FinalList.append(List)
                return
        return

    # What does this monster do and why do we need it? We do not want to assume the blocks here. Instead, we want
    # to orgnaize the blocks based on little knowledge about the system as a whole. Probably a bad idea, who knows...

    BlockInstances.append(Block(None, None, None, -1))
    # In order to use the recursive function below we need to have an ending block with a col number of -1. Don't ask

    ColSet = list(dict.fromkeys(BlockColumnNumbers))
    MaxDifference = ColSet[0] - ColSet[1]
    # Calculated the max difference between cols. This will always be the difference between the first set of unique values.
    # This max difference will always decrement by 2 per the excel code

    TracePathways([], BlockInstances, BlockInstances[0].GetCol(), MaxDifference, 2)

    for CheckList in FinalList[:]:
        for List in FinalList[:]:
            if CheckList == List:
                continue

            if len(CheckList) > len(List):
                continue

            if all(Item in List for Item in CheckList):
                FinalList.remove(CheckList)
                break
    # Remove the incomplete paths from the final list

    for List in FinalList:
        BlockTrackerInstance = BlockTracker(ExcelInstance)
        for Item in List:
            BlockTrackerInstance.LoadManual(Item)
        BlockTrackerInstances.append(BlockTrackerInstance)
    # Finally, load the sorted pathways into seperate trackers.
