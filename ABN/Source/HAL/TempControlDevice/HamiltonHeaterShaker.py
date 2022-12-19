from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Layout import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits

__DriverHandlerInstance: DriverHandler = cast(
    DriverHandler, HandlerRegistry.GetObjectByName("Driver")
)

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


class HamiltonHeaterShaker(TempControlDevice):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemTrackerInstance: LayoutItemTracker,
    ):
        TempControlDevice.__init__(
            self, Name, ComPort, True, TempLimitsInstance, LayoutItemTrackerInstance
        )
        self.HandleID: int

    def Initialize(self):
        CommandInstance = ConnectCommand(
            "", True, ConnectOptions("", self.ComPort)  # type:ignore
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        self.HandleID = CommandInstance.GetResponse().GetAdditional()["HandleID"]

        CommandInstance = SetPlateLockCommand(
            "",
            True,
            SetPlateLockOptions("", self.HandleID, 1),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        CommandInstance = SetPlateLockCommand(
            "",
            True,
            SetPlateLockOptions("", self.HandleID, 0),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

    def Deinitialize(self):
        CommandInstance = StopTemperatureControlCommand(
            "", True, StopTemperatureControlOptions("", self.HandleID)
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        CommandInstance = SetPlateLockCommand(
            "",
            True,
            SetPlateLockOptions("", self.HandleID, 0),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

    def SetTemperature(self, Temperature: float):
        CommandInstance = StartTemperatureControlCommand(
            "",
            True,
            StartTemperatureControlOptions("", self.HandleID, Temperature),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

    def GetTemperature(self) -> float:
        CommandInstance = GetTemperatureCommand(
            "",
            True,
            GetTemperatureOptions("", self.HandleID),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        return CommandInstance.GetResponse().GetAdditional()["Temperature"]

    def StartShaking(self, RPM: int):
        CommandInstance = SetPlateLockCommand(
            "",
            True,
            SetPlateLockOptions("", self.HandleID, 1),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        CommandInstance = StartShakeControlCommand(
            "",
            True,
            StartShakeControlOptions("", self.HandleID, RPM),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

    def StopShaking(self):
        CommandInstance = StopShakeControlCommand(
            "",
            True,
            StopShakeControlOptions("", self.HandleID),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        CommandInstance = SetPlateLockCommand(
            "",
            True,
            SetPlateLockOptions("", self.HandleID, 0),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

    def GetShakingSpeed(self) -> float:
        CommandInstance = GetShakingSpeedCommand(
            "",
            True,
            GetShakingSpeedOptions("", self.HandleID),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        return CommandInstance.GetResponse().GetAdditional()["ShakingSpeed"]
