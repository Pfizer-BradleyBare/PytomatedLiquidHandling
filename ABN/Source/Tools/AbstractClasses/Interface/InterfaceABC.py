from abc import ABC, abstractmethod


class InterfaceABC(ABC):
    @abstractmethod
    def Initialize(self):
        raise NotImplementedError

    @abstractmethod
    def Deinitialize(self):
        raise NotImplementedError
