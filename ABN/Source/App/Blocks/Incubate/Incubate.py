from ....API import Lid, TempControl
from ....API.Tools.Timer import TimerTracker
from ....HAL.Lid import Lid as HALLid
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


@ClassDecorator_AvailableBlock
class Incubate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)
        self.ReservedTempControlDevice: TempControlDevice | None = None
        self.ReservedLid: HALLid | None = None

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

        if self.ReservedTempControlDevice is None:
            self.ReservedTempControlDevice = TempControl.Reserve(
                ParentContainer, Temperature, ShakeSpeed, Simulate
            )
        if self.ReservedLid is None:
            self.ReservedLid = Lid.Reserve(ParentContainer, Simulate)
        # Try to reserve something

        StepContext = WorkbookInstance.GetContextTracker().GetObjectByName(
            self.GetContext()
        )

        TimerTrackerInstance: TimerTracker = (
            GetAppHandler().TimerTrackerInstance  # type:ignore
        )

        if self.ReservedTempControlDevice is None or self.ReservedLid is None:
            if Wait == "Yes":
                WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)
        # Did it work?
        # If not we need to disable this context if Wait is "Yes" Otherwise we can try again during the next step round.
        else:
            WorkbookInstance.CompletedPreprocessingBlocksTrackerInstance.ManualLoad(
                self
            )
            # No need to preprocess again!

            if Wait == "Yes":
                if not TempControl.IsReady(
                    self.ReservedTempControlDevice, Temperature, Simulate
                ):
                    WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(
                        StepContext
                    )

                    TimerTrackerInstance.ManualLoad(
                        Timer(
                            60,
                            "Waiting for TempControlDevice equilibration",
                            WorkbookInstance,
                            self,
                            PreprocessingWaitCallback,  # type:ignore
                            (1,),
                        )
                    )
                    # Start timer
            # If so we need to wait periodically until it is "equilibrated"
            else:
                if WorkbookInstance.InactiveContextTrackerInstance.IsTracked(
                    StepContext.GetName()
                ):
                    WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(
                        StepContext
                    )
            # If not then we can just proceed.

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):

        StepContext = WorkbookInstance.GetContextTracker().GetObjectByName(
            self.GetContext()
        )

        if self.ReservedTempControlDevice is None or self.ReservedLid is None:
            WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)
            return
        # If we still don't have a TempControlDevice by this point then we need to deactivate the context and wait for the darn preprocess to be successful.

        TimerTrackerInstance: TimerTracker = (
            GetAppHandler().TimerTrackerInstance  # type:ignore
        )

        Temperature = float(self.GetTemp())
        Time = float(self.GetTime())
        ShakeSpeed = int(self.GetShakeSpeed())
        ParentContainer = (
            WorkbookInstance.GetContainerTracker()
            .GetPlateTracker()
            .GetObjectByName(self.GetParentPlateName())
        )

        TempControl.Start(
            ParentContainer,
            self.ReservedTempControlDevice,
            Temperature,
            ShakeSpeed,
            WorkbookInstance.Simulate,
        )

        Lid.Cover(ParentContainer, self.ReservedLid, WorkbookInstance.Simulate)

        TimerTrackerInstance.ManualLoad(
            Timer(
                Time,
                "Incubation",
                WorkbookInstance,
                self,
                ProcessingWaitCallback,  # type:ignore
                (),
            )
        )

        WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)
        # Disable this context while we wait on the timer


def PreprocessingWaitCallback(
    WorkbookInstance: Workbook, StepInstance: Incubate, Extra: tuple
):
    Temperature = float(StepInstance.GetTemp())

    StepContext = WorkbookInstance.ContextTrackerInstance.GetObjectByName(
        StepInstance.GetContext()
    )

    TimerTrackerInstance: TimerTracker = (
        GetAppHandler().TimerTrackerInstance  # type:ignore
    )

    if StepInstance.ReservedTempControlDevice is not None:
        if TempControl.IsReady(
            StepInstance.ReservedTempControlDevice,
            Temperature,
            WorkbookInstance.Simulate,
        ):
            WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(StepContext)

        else:
            if Extra[0] != 5:
                TimerTrackerInstance.ManualLoad(
                    Timer(
                        60,
                        "Waiting for TempControlDevice equilibration",
                        WorkbookInstance,
                        StepInstance,
                        PreprocessingWaitCallback,  # type:ignore
                        (Extra[0] + 1,),
                    )
                )
            # We are only going to wait for a max of 5 minutes to prevent infinite waiting. 5 min should be plenty to EQ

            else:
                WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(
                    StepContext
                )


def ProcessingWaitCallback(
    WorkbookInstance: Workbook, StepInstance: Incubate, Extra: tuple
):
    StepContext = WorkbookInstance.ContextTrackerInstance.GetObjectByName(
        StepInstance.GetContext()
    )

    ParentContainer = (
        WorkbookInstance.GetContainerTracker()
        .GetPlateTracker()
        .GetObjectByName(StepInstance.GetParentPlateName())
    )

    Lid.Uncover(ParentContainer, StepInstance.ReservedLid)  # type:ignore

    Lid.Release(StepInstance.ReservedLid, WorkbookInstance.Simulate)  # type:ignore

    StepInstance.ReservedLid = None

    TempControl.End(
        ParentContainer,
        StepInstance.ReservedTempControlDevice,  # type:ignore
        WorkbookInstance.Simulate,
    )

    TempControl.Release(
        StepInstance.ReservedTempControlDevice, WorkbookInstance.Simulate  # type:ignore
    )

    StepInstance.ReservedTempControlDevice = None

    WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(StepContext)
