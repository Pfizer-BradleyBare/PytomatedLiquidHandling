from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC


class TempControlDeviceInterface(InterfaceABC):
    def __init__(self):
        self.HandleID: int | str
        self.CurrentTemperature: float

    @abstractmethod
    def SetTemperature(self, Temperature: float):
        ...

    @abstractmethod
    def GetTemperature(self) -> float:
        ...

    @abstractmethod
    def StartShaking(self, RPM: float):
        ...

    @abstractmethod
    def StopShaking(self):
        ...

    @abstractmethod
    def GetShakingSpeed(self) -> float:
        ...
