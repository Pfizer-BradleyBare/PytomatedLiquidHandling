from ...Driver.TemperatureControl.HeaterShaker import (
    ConnectCommand,
    ConnectOptions,
    GetShakingSpeedCommand,
    GetShakingSpeedOptions,
    GetTemperatureCommand,
    GetTemperatureOptions,
    SetPlateLockCommand,
    SetPlateLockOptions,
    StartShakeControlCommand,
    StartShakeControlOptions,
    StartTemperatureControlCommand,
    StartTemperatureControlOptions,
    StopShakeControlCommand,
    StopShakeControlOptions,
    StopTemperatureControlCommand,
    StopTemperatureControlOptions,
)
from ...Driver.Tools import CommandTracker
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterShaker(TempControlDevice):
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
            True,
            TempLimitsInstance,
            LayoutItemGroupingTrackerInstance,
        )
        self.HandleID: int

    def Initialize(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            ConnectCommand(
                "", True, ConnectOptions("", self.ComPort)  # type:ignore
            )
        )
        self.HandleID = CommandInstance.GetResponse().GetAdditional()["HandleID"]

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 1),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 0),
            )
        )

        return ReturnCommandTracker

    def Deinitialize(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            StopTemperatureControlCommand(
                "", True, StopTemperatureControlOptions("", self.HandleID)
            )
        )

        ReturnCommandTracker.ManualLoad(
            StopShakeControlCommand(
                "",
                True,
                StopShakeControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 0),
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

    def StartShaking(self, RPM: int) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 1),
            )
        )

        ReturnCommandTracker.ManualLoad(
            StartShakeControlCommand(
                "",
                True,
                StartShakeControlOptions("", self.HandleID, RPM),
            )
        )

        return ReturnCommandTracker

    def StopShaking(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            StopShakeControlCommand(
                "",
                True,
                StopShakeControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 0),
            )
        )

        return ReturnCommandTracker

    def UpdateCurrentShakingSpeed(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            GetShakingSpeedCommand(
                "",
                True,
                GetShakingSpeedOptions("", self.HandleID),
            )
        )

        self.CurrentShakingSpeed = CommandInstance.GetResponse().GetAdditional()[
            "ShakingSpeed"
        ]

        return ReturnCommandTracker
