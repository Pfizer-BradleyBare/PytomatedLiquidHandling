from ..Layout import LayoutTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterCooler(TempControlDevice):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutTrackerInstance: LayoutTracker,
    ):
        TempControlDevice.__init__(
            self, Name, ComPort, False, TempLimitsInstance, LayoutTrackerInstance
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
