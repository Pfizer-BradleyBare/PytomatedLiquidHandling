from ...Tools import InputChecker
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Dilute(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetSource(self, WorkbookInstance: Workbook) -> list[str]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1),
            [str],
            [],
        )

    def GetDiluent(self, WorkbookInstance: Workbook) -> list[str]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1),
            [str],
            [],
        )

    def GetStartingConc(self, WorkbookInstance: Workbook) -> list[int | float]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 3, self.Col + 1),
            [int, float],
            [],
        )

    def GetTargetConc(self, WorkbookInstance: Workbook) -> list[int | float]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 4, self.Col + 1),
            [int, float],
            [],
        )

    def GetTargetVolume(self, WorkbookInstance: Workbook) -> list[int | float]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 5, self.Col + 1),
            [int, float],
            [],
        )

    def GetMaxSourceVolume(self, WorkbookInstance: Workbook) -> list[int | float]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 6, self.Col + 1),
            [int, float],
            [],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        ...
