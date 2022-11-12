from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel, ExcelOperator
from ...Workbook import Workbook
from ....HAL import Hal


@ClassDecorator_AvailableBlock
class Incubate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Incubate" + str((self.Row, self.Col))

    def GetTemp(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetWaitForTempOption(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def GetTime(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 4, self.Col + 2)

    def GetShakeSpeed(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 5, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass
