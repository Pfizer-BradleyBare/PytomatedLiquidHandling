from abc import abstractmethod
from enum import Enum


class OnOff(Enum):
    On = 1
    Off = 0


class InterfaceABC:
    @abstractmethod
    def Initialize(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def Deinitialize(self) -> dict:
        raise NotImplementedError
