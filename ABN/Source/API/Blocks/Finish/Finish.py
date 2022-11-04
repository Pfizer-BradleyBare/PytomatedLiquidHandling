from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal


@ClassDecorator_AvailableBlock
class Finish(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Finish" + str((self.Row, self.Col))

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):

        WorkbookInstance.GetInactiveContextTracker().ManualLoad(
            WorkbookInstance.GetExecutingContext()
        )
        # Deactivate the current context
