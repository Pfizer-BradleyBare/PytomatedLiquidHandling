from abc import abstractmethod
from typing import Callable

from .....Driver.Tools import Command, CommandTracker
from ....Tools import InterfaceABC


class TempControlDeviceInterface(InterfaceABC):
    def __init__(self):
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
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateCurrentTemperature(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def StartShaking(
        self,
        RPM: float,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def StopShaking(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateCurrentShakingSpeed(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...
