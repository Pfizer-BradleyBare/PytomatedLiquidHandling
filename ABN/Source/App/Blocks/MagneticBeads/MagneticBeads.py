from ...Tools.Excel import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class MagneticBeads(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetMagneticBeadsPlate(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1)

    def GetStorageBuffer(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1)

    def GetStorageBufferVolume(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 3, self.Col + 1)

    def GetHoldTime(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 4, self.Col + 1)

    def GetRepitions(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 5, self.Col + 1)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        ...
