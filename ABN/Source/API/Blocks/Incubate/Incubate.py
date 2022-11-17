from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel, ExcelHandle
from ...Workbook import Workbook


@ClassDecorator_AvailableBlock
class Incubate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Incubate" + str((self.Row, self.Col))

    def GetTemp(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetWaitForTempOption(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def GetTime(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 4, self.Col + 2)

    def GetShakeSpeed(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 5, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)
