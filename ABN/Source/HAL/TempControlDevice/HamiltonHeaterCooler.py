from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Layout import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits

__DriverHandlerInstance: DriverHandler = cast(
    DriverHandler, HandlerRegistry.GetObjectByName("Driver")
)
from ...Driver.TemperatureControl.HeaterCooler.Connect import C


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

    def Initialize(self):
        raise NotImplementedError

    def Deinitialize(self):
        raise NotImplementedError

    def SetTemperature(self, Temperature: float):
        raise NotImplementedError

    def GetTemperature(self) -> float:
        raise NotImplementedError

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
