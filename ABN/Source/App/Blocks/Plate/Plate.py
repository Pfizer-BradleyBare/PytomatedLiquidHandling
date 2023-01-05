from ...Tools.Container import Plate as PlateContainer
from ...Tools.Context import Context
from ...Tools.Excel import Excel, ExcelHandle
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Plate(Block):
    PlateNames: list[str] = list()
    # we can use this to determine if a plate name is already a solution or not.

    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Plate" + str((self.Row, self.Col))

    def GetPlateName(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetPlateType(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)
            PlateName = self.GetPlateName()
            PlateFilter = self.GetPlateType()

            # Do parameter validation here

            ContextTrackerInstance = WorkbookInstance.GetActiveContextTracker()

            OldContextInstance = WorkbookInstance.GetExecutingContext()
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

            ContainerTracker = WorkbookInstance.GetContainerTracker()
            if ContainerTracker.PlateTrackerInstance.IsTracked(PlateName) is False:
                ContainerTracker.PlateTrackerInstance.ManualLoad(
                    PlateContainer(PlateName, WorkbookInstance.GetName(), PlateFilter)
                )
            # Create the container if it does not already exists
