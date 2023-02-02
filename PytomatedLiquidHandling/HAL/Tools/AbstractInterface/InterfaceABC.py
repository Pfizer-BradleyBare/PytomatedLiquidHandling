from abc import ABC, abstractmethod


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(
        self,
    ):
        ...

    @abstractmethod
    def Deinitialize(
        self,
    ):
        ...
