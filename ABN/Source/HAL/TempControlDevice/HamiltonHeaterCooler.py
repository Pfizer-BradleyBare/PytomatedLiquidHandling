from ...Driver.TemperatureControl.HeaterCooler import (
    ConnectCommand,
    ConnectOptions,
    GetTemperatureCommand,
    GetTemperatureOptions,
    StartTemperatureControlCommand,
    StartTemperatureControlOptions,
    StopTemperatureControlCommand,
    StopTemperatureControlOptions,
)
from ...Driver.Tools import CommandTracker
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterCooler(TempControlDevice):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemGroupingTrackerInstance: LayoutItemGroupingTracker,
    ):
        TempControlDevice.__init__(
            self,
            Name,
            ComPort,
            False,
            TempLimitsInstance,
            LayoutItemGroupingTrackerInstance,
        )
        self.HandleID: str

    def Initialize(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            ConnectCommand(
                "", True, ConnectOptions("", self.ComPort)  # type:ignore
            )
        )

        self.HandleID = CommandInstance.GetResponse().GetAdditional()["HandleID"]

        return ReturnCommandTracker

    def Deinitialize(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            StopTemperatureControlCommand(
                "", True, StopTemperatureControlOptions("", self.HandleID)
            )
        )

        return ReturnCommandTracker

    def SetTemperature(self, Temperature: float) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            StartTemperatureControlCommand(
                "",
                True,
                StartTemperatureControlOptions("", self.HandleID, Temperature),
            )
        )

        return ReturnCommandTracker

    def UpdateCurrentTemperature(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            GetTemperatureCommand(
                "",
                True,
                GetTemperatureOptions("", self.HandleID),
            )
        )

        self.CurrentTemperature = CommandInstance.GetResponse().GetAdditional()[
            "Temperature"
        ]

        return ReturnCommandTracker

    def StartShaking(self, RPM: float) -> CommandTracker:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def StopShaking(self) -> CommandTracker:
        return CommandTracker()

    def UpdateCurrentShakingSpeed(self) -> CommandTracker:
        self.CurrentShakingSpeed = 0
        return CommandTracker()
