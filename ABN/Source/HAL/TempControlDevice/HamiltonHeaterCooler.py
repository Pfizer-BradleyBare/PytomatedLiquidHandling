from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Layout import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits

__DriverHandlerInstance: DriverHandler = cast(
    DriverHandler, HandlerRegistry.GetObjectByName("Driver")
)
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


class HamiltonHeaterCooler(TempControlDevice):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemTrackerInstance: LayoutItemTracker,
    ):
        TempControlDevice.__init__(
            self, Name, ComPort, False, TempLimitsInstance, LayoutItemTrackerInstance
        )
        self.HandleID: str

    def Initialize(self):
        CommandInstance = ConnectCommand(
            "", True, ConnectOptions("", self.ComPort)  # type:ignore
        )
        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        self.HandleID = CommandInstance.GetResponse().GetAdditional()["HandleID"]

    def Deinitialize(self):
        CommandInstance = StopTemperatureControlCommand(
            "", True, StopTemperatureControlOptions("", self.HandleID)
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

    def StartShaking(self, RPM: float):
        raise Exception(
            "Shaking is not supported on this device. Did you check ShakingSupported?"
        )

    def StopShaking(self):
        raise Exception(
            "Shaking is not supported on this device. Did you check ShakingSupported?"
        )

    def GetShakingSpeed(self) -> float:
        raise Exception(
            "Shaking is not supported on this device. Did you check ShakingSupported?"
        )
