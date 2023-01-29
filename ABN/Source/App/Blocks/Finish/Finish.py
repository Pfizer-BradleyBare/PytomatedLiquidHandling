from ...Tools import InputChecker
from ...Tools.Context import ContextStates
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Finish(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        ContextInstance = WorkbookInstance.GetExecutingContext()

        ContextInstance.UpdateContextState(
            ContextStates.Complete,
            "Context completed successfully with a Finish block.",
        )

        WorkbookInstance.GetInactiveContextTracker().ManualLoad(ContextInstance)
        # Deactivate the current context

        return True
