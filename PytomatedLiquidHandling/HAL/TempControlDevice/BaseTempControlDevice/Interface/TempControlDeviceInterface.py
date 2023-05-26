from abc import abstractmethod

from ....Tools.AbstractClasses import InterfaceABC


class TempControlDeviceInterface(InterfaceABC):
    def __init__(self, CustomErrorHandling: bool):
        InterfaceABC.__init__(self, CustomErrorHandling)
        self.HandleID: int | str
        self.CurrentTemperature: float = 0
        self.CurrentShakingSpeed: int = 0

    def GetCurrentShakingSpeed(self) -> int:
        return self.CurrentShakingSpeed

    def GetCurrentTemperature(self) -> float:
        return self.CurrentTemperature

    @abstractmethod
    def SetTemperature(
        self,
        Temperature: float,
    ):
        ...

    @abstractmethod
    def UpdateCurrentTemperature(
        self,
    ):
        ...

    @abstractmethod
    def StartShaking(
        self,
        RPM: float,
    ):
        ...

    @abstractmethod
    def StopShaking(
        self,
    ):
        ...

    @abstractmethod
    def UpdateCurrentShakingSpeed(
        self,
    ):
        ...
