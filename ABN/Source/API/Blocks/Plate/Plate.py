from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel, ExcelOperator
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Container import Container
from ...Tools.Context import Context


@ClassDecorator_AvailableBlock
class Plate(Block):
    PlateNames: list[str] = list()
    # we can use this to determine if a plate name is already a solution or not.

    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Plate" + str((self.Row, self.Col))

    def GetPlateName(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetPlateType(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        PlateName = self.GetPlateName()
        PlateFilter = self.GetPlateType()

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()
        InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()

        OldContextInstance = WorkbookInstance.GetExecutingContext()
        NewContextInstance = Context(
            OldContextInstance.GetName() + ":" + PlateName,
            OldContextInstance.GetDispenseWellSequenceTracker(),
            OldContextInstance.GetDispenseWellSequenceTracker(),
            OldContextInstance.GetWellFactorTracker(),
        )
        # We only bring forward the dispense well sequences
        InactiveContextTrackerInstance.ManualLoad(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewContextInstance)
        WorkbookInstance.SetExecutingContext(NewContextInstance)
        # Deactivate the previous context and active this new context

        ContainerTracker = WorkbookInstance.GetContainerTracker()

        PlateContainerInstance = Container(PlateName, PlateFilter)
        if ContainerTracker.IsTracked(PlateContainerInstance) is False:
            ContainerTracker.ManualLoad(PlateContainerInstance)
        # Create the container if it does not already exists
