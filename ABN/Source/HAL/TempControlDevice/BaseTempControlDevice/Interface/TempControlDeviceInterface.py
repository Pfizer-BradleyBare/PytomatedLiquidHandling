from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC


class TempControlDeviceInterface(InterfaceABC):
    def __init__(self):
        self.HandleID: int | str
        self.CurrentTemperature: float = 0
        self.CurrentShakingSpeed: int = 0

    @abstractmethod
    def SetTemperature(self, Temperature: float):
        ...

    @abstractmethod
    def UpdateCurrentTemperature(self):
        ...

    def GetCurrentTemperature(self) -> float:
        return self.CurrentTemperature

    @abstractmethod
    def StartShaking(self, RPM: float):
        ...

    @abstractmethod
    def StopShaking(self):
        ...

    @abstractmethod
    def UpdateCurrentShakingSpeed(self):
        ...

    def GetCurrentShakingSpeed(self) -> int:
        return self.CurrentShakingSpeed
