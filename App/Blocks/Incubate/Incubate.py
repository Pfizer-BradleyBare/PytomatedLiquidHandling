from PytomatedLiquidHandling.API import Lid, TempControl
from PytomatedLiquidHandling.HAL.Lid import Lid as HALLid
from PytomatedLiquidHandling.HAL.TempControlDevice.BaseTempControlDevice import (
    TempControlDevice,
)

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
class Incubate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)
        self.ReservedTempControlDevice: TempControlDevice | None = None
        self.ReservedLid: HALLid | None = None

        # Params
        self.Temperature = BlockParameter.Item[str | int | float](
            self, 1, ["Ambient"] + [Val / 10.0 for Val in range(0, 1100)]
        )
        self.WaitForTemp = BlockParameter.Item[str](self, 2, ["Yes", "No"])
        self.Time = BlockParameter.Item[int | float](self, 3)
        self.ShakeSpeed = BlockParameter.Item[int | float](self, 4)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:

        Temperature = self.Temperature.Read(WorkbookInstance)
        Wait = self.WaitForTemp.Read(WorkbookInstance)
        ShakeSpeed = self.ShakeSpeed.Read(WorkbookInstance)
        ParentContainer = (
            WorkbookInstance.GetContainerTracker()
            .GetPlateTracker()
            .GetObjectByName(self.GetParentPlateName())
        )

        from ...Handler import GetHandler

        RunType = WorkbookInstance.RunType

        StepContext = WorkbookInstance.GetContextTracker().GetObjectByName(
            self.GetContext()
        )

        TimerTrackerInstance = GetHandler().TimerTrackerInstance

        if type(Temperature) == str and Temperature == "Ambient":

            if self.ReservedLid is None:
                self.ReservedLid = Lid.Reserve(ParentContainer, RunType)
            # Try to reserve something
            if self.ReservedLid is None:
                return False
            # Try again next round
            else:
                return True

        else:

            if self.ReservedTempControlDevice is None:
                self.ReservedTempControlDevice = TempControl.Reserve(
                    ParentContainer, float(Temperature), int(ShakeSpeed), RunType
                )
            if self.ReservedLid is None:
                self.ReservedLid = Lid.Reserve(ParentContainer, RunType)
            # Try to reserve something

            if self.ReservedTempControlDevice is None or self.ReservedLid is None:
                if Wait == "Yes":
                    WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(
                        StepContext
                    )

                return False
            # Did it work?
            # If not we need to disable this context if Wait is "Yes" Otherwise we can try again during the next step round.
            else:

                if Wait == "Yes":
                    if not TempControl.IsReady(
                        self.ReservedTempControlDevice, float(Temperature), RunType
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

                return True
                # No need to preprocess again!

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        WorkbookInstance.PreprocessingBlocksTrackerInstance.ManualLoad(self)
        # This block requires preprocessing. Let's add it to the list

        from ...Handler import GetHandler

        TimerTrackerInstance = GetHandler().TimerTrackerInstance

        StepContext = WorkbookInstance.GetContextTracker().GetObjectByName(
            self.GetContext()
        )

        Temperature = self.Temperature.Read(WorkbookInstance)
        Time = self.Time.Read(WorkbookInstance)
        ShakeSpeed = self.ShakeSpeed.Read(WorkbookInstance)
        ParentContainer = (
            WorkbookInstance.GetContainerTracker()
            .GetPlateTracker()
            .GetObjectByName(self.GetParentPlateName())
        )

        if type(Temperature) == str and Temperature == "Ambient":
            if self.ReservedLid is None:
                WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)
                return False
            # If we still don't have a TempControlDevice by this point then we need to deactivate the context and wait for the darn preprocess to be successful.
        else:
            if self.ReservedTempControlDevice is None or self.ReservedLid is None:
                WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)
                return False

            else:

                TempControl.Start(
                    ParentContainer,
                    self.ReservedTempControlDevice,  # type:ignore
                    float(Temperature),
                    ShakeSpeed,
                    WorkbookInstance.RunType,
                )

        Lid.Cover(ParentContainer, self.ReservedLid, WorkbookInstance.RunType)

        TimerTrackerInstance.ManualLoad(
            Timer(
                Time * 60,
                "Incubation",
                WorkbookInstance,
                self,
                ProcessingWaitCallback,  # type:ignore
                (),
            )
        )

        WorkbookInstance.InactiveContextTrackerInstance.ManualLoad(StepContext)
        # Disable this context while we wait on the timer

        return True


def PreprocessingWaitCallback(
    WorkbookInstance: Workbook, StepInstance: Incubate, Extra: tuple
):
    Temperature = StepInstance.Temperature.Read(WorkbookInstance)

    StepContext = WorkbookInstance.ContextTrackerInstance.GetObjectByName(
        StepInstance.GetContext()
    )

    from ...Handler import GetHandler

    TimerTrackerInstance = GetHandler().TimerTrackerInstance

    if StepInstance.ReservedTempControlDevice is not None:
        if TempControl.IsReady(
            StepInstance.ReservedTempControlDevice,
            float(Temperature),
            WorkbookInstance.RunType,
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

    Temperature = StepInstance.Temperature.Read(WorkbookInstance)
    ParentContainer = (
        WorkbookInstance.GetContainerTracker()
        .GetPlateTracker()
        .GetObjectByName(StepInstance.GetParentPlateName())
    )

    Lid.Uncover(ParentContainer, StepInstance.ReservedLid)  # type:ignore

    Lid.Release(StepInstance.ReservedLid, WorkbookInstance.Simulate)  # type:ignore

    StepInstance.ReservedLid = None

    if type(Temperature) != str and Temperature != "Ambient":

        TempControl.End(
            ParentContainer,
            StepInstance.ReservedTempControlDevice,  # type:ignore
            WorkbookInstance.RunType,
        )

        TempControl.Release(
            StepInstance.ReservedTempControlDevice,  # type:ignore
            WorkbookInstance.RunType,
        )

        StepInstance.ReservedTempControlDevice = None

    WorkbookInstance.InactiveContextTrackerInstance.ManualUnload(StepContext)
