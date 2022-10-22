from .Block import BlockObjectCreationWrapper, Block
from .BlockTracker import BlockTracker
from ....Tools import Excel
from ...Blocks import *  # noqa F403
from ....Server.Tools import LOG


def Load(BlockTrackerInstance: BlockTracker, ExcelInstance: Excel):
    MethodSheet = ExcelInstance.ReadMethodSheet()

    Rows = len(MethodSheet)
    Cols = len(MethodSheet[0])

    BlockInstancesList: list[list[Block]] = list()

    for ColIndex in range(0, Cols):
        Temp = list()
        for RowIndex in range(0, Rows):
            Name: str = MethodSheet[RowIndex][ColIndex]

            if Name is None:
                continue

            if type(Name) is not str:
                continue

            if " - (Click Here to Update)" not in Name:
                continue

            Name = Name.replace(" - (Click Here to Update)", "")

            Temp.append(
                BlockObjectCreationWrapper(ExcelInstance, Name, RowIndex, ColIndex)
            )

        if len(Temp) != 0:
            BlockInstancesList.append(Temp)
    # Put blocks in a list of lists that is loaded according to the column of the block

    TempBlockInstancesList = list()
    for BlockInstances in BlockInstancesList:
        Temp = list()
        for BlockInstance in BlockInstances:
            if type(BlockInstance).__name__ != SplitPlate.__name__:  # noqa F405
                Temp.append(BlockInstance)
            else:
                Temp.append(BlockInstance)
                TempBlockInstancesList.append(Temp)
                Temp = list()
        if len(Temp) != 0:
            TempBlockInstancesList.append(Temp)
    BlockInstancesList = TempBlockInstancesList
    # Traverse each list and split the list if a split plate is present.

    Pathways = list()
    for BlockInstances in BlockInstancesList:
        BlockInstance = BlockInstances[0]
        if type(BlockInstance).__name__ != Plate.__name__:  # noqa F405
            raise Exception("Method is not valid!")
        else:
            PlateName = BlockInstance.GetPlateName()
            if PlateName in Pathways:
                raise Exception("Method is not valid!")
            Pathways.append(BlockInstance.GetPlateName())
    # Check that the starting Block is a Plate and the name is unique in each list

    for BlockInstances in BlockInstancesList:
        BlockInstance = BlockInstances[-1]
        if type(BlockInstance).__name__ == SplitPlate.__name__:  # noqa F405
            if BlockInstance.GetPathway1Name() not in Pathways:
                raise Exception("Pathways are not referenced correctly!")
            if BlockInstance.GetPathway2Name() not in Pathways:
                raise Exception("Pathways are not referenced correctly!")
    # Now we need to confirm that a split plate references the correct pathways

    MethodPathways = list()

    # This will effectively connect our blocks into a wonderful tree in order of correct execution :)
    # It will also make complete pathways from start to end. Neato!
    def TraversePathways(
        OutputList, CollectionList, TraversalList, PathwaysList, PreviousBlock
    ):
        for BlockInstance in TraversalList:
            CollectionList.append(BlockInstance)
            BlockInstance.SetParentNode(PreviousBlock)
            PreviousBlock = BlockInstance

            if type(BlockInstance).__name__ == SplitPlate.__name__:  # noqa F405
                Pathways = [
                    BlockInstance.GetPathway1Name(),
                    BlockInstance.GetPathway2Name(),
                ]
                for Pathway in PathwaysList[:]:
                    if Pathway[0].GetPlateName() in Pathways:
                        PathwaysList.remove(Pathway)
                        TraversePathways(
                            OutputList,
                            CollectionList[:],
                            Pathway,
                            PathwaysList,
                            PreviousBlock,
                        )
                return
            # We need to traverse both pathways
        OutputList.append(CollectionList)

    StartingPathway = BlockInstancesList[0]  # Load with something random
    for BlockInstances in BlockInstancesList:
        if BlockInstances[0].GetRow() < StartingPathway[0].GetRow():
            StartingPathway = BlockInstances
    BlockInstancesList.remove(StartingPathway)
    # Find first traversal pathway.

    TraversePathways(MethodPathways, list(), StartingPathway, BlockInstancesList, None)
    # Now we need to create a seperate list for each pathway... This will need to happen recursively. Kill me now

    for Pathway in MethodPathways:
        if type(Pathway[-1]).__name__ != Finish.__name__:  # noqa F405
            raise Exception("All pathways must end with a finish step")
    # Check that each pathway ends with a finish step.

    # LOL IDK
    # Unique
    OrganizedBlocks = list()
    for Pathway in MethodPathways:
        for BlockInstance in Pathway:
            if BlockInstance not in OrganizedBlocks:
                BlockTrackerInstance.LoadManual(BlockInstance)
                OrganizedBlocks.append(BlockInstance)
    # Now get each block uniquely from the list of blocks. This is relatively in order which is what we want
