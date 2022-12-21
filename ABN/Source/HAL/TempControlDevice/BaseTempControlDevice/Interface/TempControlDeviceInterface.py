from abc import abstractmethod

from .....Driver.Tools import CommandTracker
from .....Tools.AbstractClasses import InterfaceABC


class TempControlDeviceInterface(InterfaceABC):
    def __init__(self):
        self.HandleID: int | str
        self.CurrentTemperature: float = 0
        self.CurrentShakingSpeed: int = 0

    @abstractmethod
    def SetTemperature(self, Temperature: float) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateCurrentTemperature(self) -> CommandTracker:
        ...

    def GetCurrentTemperature(self) -> float:
        return self.CurrentTemperature

    @abstractmethod
    def StartShaking(self, RPM: float) -> CommandTracker:
        ...

    @abstractmethod
    def StopShaking(self) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateCurrentShakingSpeed(self) -> CommandTracker:
        ...

    def GetCurrentShakingSpeed(self) -> int:
        return self.CurrentShakingSpeed
