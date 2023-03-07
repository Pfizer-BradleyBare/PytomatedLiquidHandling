from ...Tools import BlockParameter
from ...Tools.Container import Plate as PlateContainer
from ...Tools.Context import Context
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Plate(Block):
    PlateNames: list[str] = list()
    # we can use this to determine if a plate name is already a solution or not.

    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.PlateName = BlockParameter.Item[str](self, 1)
        self.PlateType = BlockParameter.Item[str](self, 2)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        PlateName = self.PlateName.Read(WorkbookInstance)
        PlateFilter = self.PlateType.Read(WorkbookInstance)

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.ContextTrackerInstance

        OldContextInstance = WorkbookInstance.ExecutingContextInstance
        NewContextInstance = Context(
            OldContextInstance.GetName() + ":" + PlateName,
            OldContextInstance.GetDispenseWellSequenceTracker(),
            OldContextInstance.GetDispenseWellSequenceTracker(),
            OldContextInstance.GetWellFactorTracker(),
        )
        # We only bring forward the dispense well sequences

        ContextTrackerInstance.ManualUnload(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewContextInstance)
        WorkbookInstance.SetExecutingContext(NewContextInstance)
        # Deactivate the previous context and active this new context by removing and new adding

        ContainerTracker = WorkbookInstance.ContainerTrackerInstance
        if ContainerTracker.PlateTrackerInstance.IsTracked(PlateName) is False:
            ContainerTracker.PlateTrackerInstance.ManualLoad(
                PlateContainer(PlateName, WorkbookInstance.GetName(), PlateFilter)
            )
        # Create the container if it does not already exists

        return True
