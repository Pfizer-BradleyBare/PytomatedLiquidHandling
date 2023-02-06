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

    def GetTime(self, WorkbookInstance: Workbook) -> int | float:
        return InputChecker.CheckAndConvertItem(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1),
            [int, float],
            [],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        from ...Handler import GetHandler

        TimerTrackerInstance = GetHandler().TimerTrackerInstance

        StepContext = WorkbookInstance.GetContextTracker().GetObjectByName(
            self.GetContext()
        )

        WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)

        TimerTrackerInstance.ManualLoad(
            Timer(
                self.GetTime(WorkbookInstance) * 60,
                "Pause",
                WorkbookInstance,
                self,
                PauseProcessCallback,  # type:ignore
                (),
            )
        )

        return True


def PauseProcessCallback(WorkbookInstance: Workbook, StepInstance: Pause, Extra: tuple):
    StepContext = WorkbookInstance.GetContextTracker().GetObjectByName(
        StepInstance.GetContext()
    )

    WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(StepContext)
