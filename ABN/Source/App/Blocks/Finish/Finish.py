from ....Tools import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Finish(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Finish" + str((self.Row, self.Col))

    def Preprocess(self, WorkbookInstance: Workbook):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):

        WorkbookInstance.GetInactiveContextTracker().ManualLoad(
            WorkbookInstance.GetExecutingContext()
        )
        # Deactivate the current context
