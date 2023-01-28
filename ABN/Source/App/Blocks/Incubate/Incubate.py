from ....API.TempControl import End, IsReady, Release, Reserve, Start
from ....API.Tools.Timer import TimerTracker
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ....Server.Globals import GetAppHandler
from ...Tools.Excel import Excel
from ...Tools.Timer import Timer
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


def PreprocessingWaitCallback(
    WorkbookInstance: Workbook, BlockInstance: Block, Extra: tuple
):
    BlockContext = WorkbookInstance.ContextTrackerInstance.GetObjectByName(
        BlockInstance.GetContext()
    )

    WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(BlockContext)


@ClassDecorator_AvailableBlock
class Incubate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)
        self.ReservedTempControlDevice: TempControlDevice | None = None

    def GetTemp(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1)

    def GetWaitForTempOption(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1)

    def GetTime(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 3, self.Col + 1)

    def GetShakeSpeed(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 4, self.Col + 1)

    def Preprocess(self, WorkbookInstance: Workbook):

        Temperature = float(self.GetTemp())
        Wait = self.GetWaitForTempOption()
        ShakeSpeed = int(self.GetShakeSpeed())
        ParentContainer = (
            WorkbookInstance.GetContainerTracker()
            .GetPlateTracker()
            .GetObjectByName(self.GetParentPlateName())
        )

        Simulate = WorkbookInstance.Simulate

        self.ReservedTempControlDevice = Reserve(
            ParentContainer, Temperature, ShakeSpeed, Simulate
        )
        # Try to reserve something

        ExecutingContext = WorkbookInstance.GetExecutingContext()

        TimerTrackerInstance: TimerTracker = (
            GetAppHandler().TimerTrackerInstance  # type:ignore
        )

        if self.ReservedTempControlDevice is None:
            if Wait == "Yes":
                WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(
                    ExecutingContext
                )
        # Did it work?
        # If not we need to disable this context if Wait is "Yes" Otherwise we can try again during the next step round.
        else:
            if Wait == "Yes":
                if not IsReady(self.ReservedTempControlDevice, Temperature, Simulate):
                    WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(
                        ExecutingContext
                    )

                    TimerTrackerInstance.ManualLoad(
                        Timer(
                            60,
                            "Waiting for TempControlDevice equilibration",
                            WorkbookInstance,
                            self,
                            PreprocessingWaitCallback,
                            (1,),
                        )
                    )
                    # Start timer
            # If so we need to wait periodically until it is "equilibrated"

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        ...
