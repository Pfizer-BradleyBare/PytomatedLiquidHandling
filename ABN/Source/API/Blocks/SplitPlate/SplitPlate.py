from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Context import (
    Context,
    WellFactorTracker,
    WellSequencesTracker,
    WellFactor,
    WellSequences,
)


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

        OldContext = WorkbookInstance.GetExecutingContext()
        NewPathway1Context = Context(
            OldContext.GetName() + ":" + Pathway1Name,
            WellSequencesTracker(),
            WellSequencesTracker(),
            WellFactorTracker(),
        )
        NewPathway2Context = Context(
            OldContext.GetName() + ":" + Pathway2Name,
            WellSequencesTracker(),
            WellSequencesTracker(),
            WellFactorTracker(),
        )
        #New Contexts. Now we need to load them

        for (
            Pathway,
            WellFactorInstance,
            AspirateWellSequencesInstance,
            DispenseWellSequencesInstance,
        ) in zip(
            PathwayChoice,
            OldContext.GetWellFactorTracker().GetObjectsAsList(),
            OldContext.GetAspirateWellSequencesTracker().GetObjectsAsList(),
            OldContext.GetDispenseWellSequencesTracker().GetObjectsAsList(),
        ):
            if Pathway == Pathway1Name:
                pass
            elif Pathway == Pathway2Name:


        # Create the contexts here

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()
        InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()
        ContainerTracker = WorkbookInstance.GetContainerTracker()

        PlateContainerInstance = Container(PlateName, PlateFilter)
        if ContainerTracker.IsTracked(PlateContainerInstance) == False:
            ContainerTracker.ManualLoad(PlateContainerInstance)
        # Create the container if it does not already exists

        OldContextInstance = WorkbookInstance.GetExecutingContext()
        NewContextInstance = Context(
            OldContextInstance.GetName() + ":" + PlateName,
            OldContextInstance.GetAspirateWellSequencesTracker(),
            OldContextInstance.GetDispenseWellSequencesTracker,
            OldContextInstance.GetWellFactorTracker(),
        )
        InactiveContextTrackerInstance.ManualLoad(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewContextInstance)
        WorkbookInstance.SetExecutingContext(NewContextInstance)
        # Deactivate the previous context and active this new context
