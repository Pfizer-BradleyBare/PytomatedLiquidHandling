from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Tools.Timer import Timer
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Pause(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.Time = BlockParameter.Item[int | float](self, 1)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        from ...Handler import GetHandler

        TimerTrackerInstance = GetHandler().TimerTrackerInstance

        StepContext = WorkbookInstance.ContextTrackerInstance.GetObjectByName(
            self.GetContext()
        )

        WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)

        TimerTrackerInstance.ManualLoad(
            Timer(
                self.Time.Read(WorkbookInstance) * 60,
                "Pause",
                WorkbookInstance,
                self,
                PauseProcessCallback,  # type:ignore
                (),
            )
        )

        return True


def PauseProcessCallback(WorkbookInstance: Workbook, StepInstance: Pause, Extra: tuple):
    StepContext = WorkbookInstance.ContextTrackerInstance.GetObjectByName(
        StepInstance.GetContext()
    )

    WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(StepContext)
