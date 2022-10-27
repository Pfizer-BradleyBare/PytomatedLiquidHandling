from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Context import (
    Context,
    WellFactorTracker,
    WellSequencesTracker,
    WellFactor,
)
from ...Tools.Container import Container
from ...Blocks import Plate


@ClassDecorator_AvailableBlock
class SplitPlate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Split Plate" + str((self.Row, self.Col))

    def GetPathwayChoice(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetPathway1Name(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetPathway2Name(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        Pathway1Name = self.GetPathway1Name()
        Pathway2Name = self.GetPathway2Name()
        PathwayChoice = self.GetPathwayChoice()

        if WorkbookInstance.GetWorklist().IsWorklistColumn(PathwayChoice) is True:
            PathwayChoice = WorkbookInstance.GetWorklist().ReadWorklistColumn(
                PathwayChoice
            )
        else:
            PathwayChoice = WorkbookInstance.GetWorklist().ConvertToWorklistColumn(
                PathwayChoice
            )

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()
        InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()

        OldContextInstance = WorkbookInstance.GetExecutingContext()
        NewPathway1ContextInstance = Context(
            OldContextInstance.GetName() + ":" + Pathway1Name,
            WellSequencesTracker(),
            WellSequencesTracker(),
            WellFactorTracker(),
        )
        NewPathway2ContextInstance = Context(
            OldContextInstance.GetName() + ":" + Pathway2Name,
            WellSequencesTracker(),
            WellSequencesTracker(),
            WellFactorTracker(),
        )
        # New Contexts. Now we need to load them

        for (
            WellFactorInstance,
            AspirateWellSequencesInstance,
            DispenseWellSequencesInstance,
        ) in zip(
            OldContextInstance.GetWellFactorTracker().GetObjectsAsList(),
            OldContextInstance.GetAspirateWellSequencesTracker().GetObjectsAsList(),
            OldContextInstance.GetDispenseWellSequencesTracker().GetObjectsAsList(),
        ):
            if not (
                WellFactorInstance.GetName()
                == AspirateWellSequencesInstance.GetName()
                == DispenseWellSequencesInstance.GetName()
            ):
                raise Exception(
                    "Wells are not the same across factors and sequences"
                )  # This should never happen

            Pathway = PathwayChoice[WellFactorInstance.GetName()]

            if Pathway.lower() == Pathway1Name.lower():
                NewPathway1ContextInstance.GetWellFactorTracker().ManualLoad(
                    WellFactorInstance
                )
                NewPathway1ContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                    AspirateWellSequencesInstance
                )
                NewPathway1ContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                    DispenseWellSequencesInstance
                )

            elif Pathway.lower() == Pathway2Name.lower():
                NewPathway2ContextInstance.GetWellFactorTracker().ManualLoad(
                    WellFactorInstance
                )
                NewPathway2ContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                    AspirateWellSequencesInstance
                )
                NewPathway2ContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                    DispenseWellSequencesInstance
                )

            elif Pathway.lower() == "Concurrent".lower():
                NewPathway1ContextInstance.GetWellFactorTracker().ManualLoad(
                    WellFactorInstance
                )
                NewPathway1ContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                    AspirateWellSequencesInstance
                )
                NewPathway1ContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                    DispenseWellSequencesInstance
                )

                NewPathway2ContextInstance.GetWellFactorTracker().ManualLoad(
                    WellFactorInstance
                )
                NewPathway2ContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                    AspirateWellSequencesInstance
                )
                NewPathway2ContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                    DispenseWellSequencesInstance
                )

            else:  # Pathway.lower() == "Split".lower():
                NewPathway1ContextInstance.GetWellFactorTracker().ManualLoad(
                    WellFactor(
                        WellFactorInstance.GetName(),
                        WellFactorInstance.GetFactor() * 0.5,
                    )
                )
                NewPathway1ContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                    AspirateWellSequencesInstance
                )
                NewPathway1ContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                    DispenseWellSequencesInstance
                )

                NewPathway2ContextInstance.GetWellFactorTracker().ManualLoad(
                    WellFactor(
                        WellFactorInstance.GetName(),
                        WellFactorInstance.GetFactor() * 0.5,
                    )
                )
                NewPathway2ContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                    AspirateWellSequencesInstance
                )
                NewPathway2ContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                    DispenseWellSequencesInstance
                )
        # Create the contexts here

        InactiveContextTrackerInstance.ManualLoad(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewPathway1ContextInstance)
        ContextTrackerInstance.ManualLoad(NewPathway2ContextInstance)
        WorkbookInstance.SetExecutingContext(NewPathway1ContextInstance)
        # Deactivate the previous context and active this new context
        # We always execute pathway 1 first. Just easier to remember as 1st is 1st

        ContainerTracker = WorkbookInstance.GetContainerTracker()

        Children: list[Plate] = self.GetChildren()
        for Child in Children:
            ContainerTracker.ManualLoad(
                Container(Child.GetPlateName(), Child.GetPlateType())
            )
            WorkbookInstance.GetExecutedBlocksTracker().ManualLoad(Child)
            # We are executing these blocks in the split plate step so we need to track them as executed.
        # Create the containers for the plate blocks followin the split plate
        # Split plate pathways must be unique. Thus we are guarenteed that the container does not already exist
