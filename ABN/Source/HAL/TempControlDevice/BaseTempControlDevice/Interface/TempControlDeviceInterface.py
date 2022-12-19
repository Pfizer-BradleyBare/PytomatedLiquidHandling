from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC


class TempControlDeviceInterface(InterfaceABC):
    def __init__(self):
        self.HandleID: int | str
        self.CurrentTemperature: float

    @abstractmethod
    def SetTemperature(self, Temperature: float):
        raise NotImplementedError

    @abstractmethod
    def GetTemperature(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def StartShaking(self, RPM: float):
        raise NotImplementedError

    @abstractmethod
    def StopShaking(self):
        raise NotImplementedError

    @abstractmethod
    def GetShakingSpeed(self) -> float:
        raise NotImplementedError
