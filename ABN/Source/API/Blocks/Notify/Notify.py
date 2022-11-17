from ....Tools import Excel, ExcelHandle
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Notify(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Notify" + str((self.Row, self.Col))

    def GetWaitOnUserOption(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetSubject(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def GetMessage(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 4, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)
