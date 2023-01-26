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

    def Initialize(
        self,
    ):

        try:
            Command = ConnectCommand(
                "",
                ConnectOptions("", self.ComPort),  # type:ignore
                True,
            )

            Command.Execute()

            self.HandleID = Command.GetResponse().GetAdditional()["HandleID"]
        except:
            ...

        try:
            SetPlateLockCommand(
                "", SetPlateLockOptions("", self.HandleID, 1), True
            ).Execute()
        except:
            ...

        try:
            SetPlateLockCommand(
                "", SetPlateLockOptions("", self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def Deinitialize(
        self,
    ):

        try:
            StopTemperatureControlCommand(
                "", StopTemperatureControlOptions("", self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            StopShakeControlCommand(
                "", StopShakeControlOptions("", self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            SetPlateLockCommand(
                "", SetPlateLockOptions("", self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
    ):

        try:
            StartTemperatureControlCommand(
                "", StartTemperatureControlOptions("", self.HandleID, Temperature), True
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
    ):
        try:
            Command = GetTemperatureCommand(
                "", GetTemperatureOptions("", self.HandleID), True
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetResponse().GetAdditional()[
                "Temperature"
            ]
        except:
            ...

    def StartShaking(
        self,
        RPM: int,
    ):

        try:
            SetPlateLockCommand(
                "", SetPlateLockOptions("", self.HandleID, 1), True
            ).Execute()
        except:
            ...

        try:
            StartShakeControlCommand(
                "", StartShakeControlOptions("", self.HandleID, RPM), True
            ).Execute()
        except:
            ...

    def StopShaking(
        self,
    ):

        try:
            StopShakeControlCommand(
                "", StopShakeControlOptions("", self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            SetPlateLockCommand(
                "", SetPlateLockOptions("", self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def UpdateCurrentShakingSpeed(
        self,
    ):

        try:
            Command = GetShakingSpeedCommand(
                "", GetShakingSpeedOptions("", self.HandleID), True
            )

            Command.Execute()

            self.CurrentShakingSpeed = Command.GetResponse().GetAdditional()[
                "ShakingSpeed"
            ]
        except:
            ...
