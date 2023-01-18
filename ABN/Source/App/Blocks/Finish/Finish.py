from ...Tools.Context import ContextStates
from ...Tools.Excel import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Finish(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def Preprocess(self, WorkbookInstance: Workbook):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):

        ContextInstance = WorkbookInstance.GetExecutingContext()

        ContextInstance.UpdateContextState(
            ContextStates.Complete,
            "Context completed successfully with a Finish block.",
        )

        WorkbookInstance.GetActiveContextTracker().ManualUnload(ContextInstance)
        WorkbookInstance.GetInactiveContextTracker().ManualLoad(ContextInstance)
        # Deactivate the current context
