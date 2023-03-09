from typing import cast

from ...Blocks import Plate
from ...Tools import BlockParameter
from ...Tools.Container import Plate as PlateContainer
from ...Tools.Context import Context, WellFactor, WellFactorTracker, WellSequenceTracker
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class SplitPlate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.PathwayChoice = BlockParameter.List[str](self, 1)
        self.Pathway1Name = BlockParameter.Item[str](self, 2)
        self.Pathway2Name = BlockParameter.Item[str](self, 3)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        Pathway1Name = self.Pathway1Name.Read(WorkbookInstance)
        Pathway2Name = self.Pathway2Name.Read(WorkbookInstance)
        PathwayChoices = self.PathwayChoice.Read(WorkbookInstance)

        ContextTrackerInstance = WorkbookInstance.ContextTrackerInstance

        OldContextInstance = WorkbookInstance.ExecutingContextInstance
        NewPathway1ContextInstance = Context(
            OldContextInstance.GetName() + ":" + Pathway1Name,
            WellSequenceTracker(),
            WellSequenceTracker(),
            WellFactorTracker(),
        )
        NewPathway2ContextInstance = Context(
            OldContextInstance.GetName() + ":" + Pathway2Name,
            WellSequenceTracker(),
            WellSequenceTracker(),
            WellFactorTracker(),
        )
        # New Contexts. Now we need to load them

        for WellNumber in range(
            1, WorkbookInstance.WorklistInstance.GetNumSamples() + 1
        ):

            PathwayChoice = PathwayChoices[WellNumber - 1]

            Factor = (
                OldContextInstance.GetWellFactorTracker()
                .GetObjectByName(WellNumber)
                .GetFactor()
            )
            SequenceInstance = (
                OldContextInstance.GetDispenseWellSequenceTracker().GetObjectByName(
                    WellNumber
                )
            )

            if PathwayChoice == Pathway1Name:
                Pathway1Factor = Factor * 1.0
                Pathway2Factor = Factor * 0.0

            elif PathwayChoice == Pathway2Name:
                Pathway1Factor = Factor * 0.0
                Pathway2Factor = Factor * 1.0

            elif PathwayChoice == "Split":
                Pathway1Factor = Factor * 0.5
                Pathway2Factor = Factor * 0.5

            else:  # PathwayChoice == "Concurrent":
                Pathway1Factor = Factor * 1.0
                Pathway2Factor = Factor * 1.0

            # Pathway 1 context
            NewPathway1ContextInstance.GetAspirateWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway1ContextInstance.GetDispenseWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway1ContextInstance.GetWellFactorTracker().ManualLoad(
                WellFactor(WellNumber, Pathway1Factor)
            )

            # Pathway 2 context
            NewPathway2ContextInstance.GetAspirateWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway2ContextInstance.GetDispenseWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway2ContextInstance.GetWellFactorTracker().ManualLoad(
                WellFactor(WellNumber, Pathway2Factor)
            )

        # Create the contexts here

        ContextTrackerInstance.ManualUnload(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewPathway1ContextInstance)
        ContextTrackerInstance.ManualLoad(NewPathway2ContextInstance)
        WorkbookInstance.SetExecutingContext(NewPathway1ContextInstance)
        # Deactivate the previous context and active this new context
        # We always execute pathway 1 first. Just easier to remember cause it is like reading a book. Left to right

        ContainerTracker = WorkbookInstance.ContainerTrackerInstance

        Children: list[Plate] = cast(list[Plate], self.GetChildren())
        for Child in Children:
            ContainerTracker.PlateTrackerInstance.ManualLoad(
                PlateContainer(
                    Child.PlateName.Read(WorkbookInstance),
                    WorkbookInstance.GetName(),
                    Child.PlateType.Read(WorkbookInstance),
                )
            )
            WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(Child)
            # We are executing these blocks in the split plate step so we need to track them as executed.
        # Create the containers for the plate blocks followin the split plate
        # Split plate pathways must be unique. Thus we are guarenteed that the container does not already exist

        return True
