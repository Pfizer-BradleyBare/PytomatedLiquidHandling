from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel, ExcelHandle
from ...Workbook import Workbook


@ClassDecorator_AvailableBlock
class Dilute(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Dilute" + str((self.Row, self.Col))

    def GetSource(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetDestination(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def GetStartingConc(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 4, self.Col + 2)

    def GetTargetConc(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 5, self.Col + 2)

    def GetTargetVolume(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 6, self.Col + 2)

    def GetMaxSourceVolume(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 7, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)
