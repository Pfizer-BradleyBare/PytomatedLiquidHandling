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

    def Initialize(self):
        raise NotImplementedError

    def Deinitialize(self):
        raise NotImplementedError

    def SetTemperature(self, Temperature: float):
        raise NotImplementedError

    def GetTemperature(self) -> float:
        raise NotImplementedError

    def StartShaking(self, RPM: float):
        raise NotImplementedError

    def StopShaking(self):
        raise NotImplementedError

    def GetShakingSpeed(self) -> float:
        raise NotImplementedError
