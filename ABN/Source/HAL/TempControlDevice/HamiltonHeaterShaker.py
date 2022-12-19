from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
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
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Layout import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


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
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

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
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

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
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

        CommandInstance = StartTemperatureControlCommand(
            "",
            True,
            StartTemperatureControlOptions("", self.HandleID, Temperature),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

    def GetTemperature(self) -> float:
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

        CommandInstance = GetTemperatureCommand(
            "",
            True,
            GetTemperatureOptions("", self.HandleID),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        return CommandInstance.GetResponse().GetAdditional()["Temperature"]

    def StartShaking(self, RPM: int):
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

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
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

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
        __DriverHandlerInstance: DriverHandler = cast(
            DriverHandler, HandlerRegistry.GetObjectByName("Driver")
        )

        CommandInstance = GetShakingSpeedCommand(
            "",
            True,
            GetShakingSpeedOptions("", self.HandleID),
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        return CommandInstance.GetResponse().GetAdditional()["ShakingSpeed"]
