from abc import ABC, abstractmethod


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def Deinitialize(self) -> dict:
        raise NotImplementedError
