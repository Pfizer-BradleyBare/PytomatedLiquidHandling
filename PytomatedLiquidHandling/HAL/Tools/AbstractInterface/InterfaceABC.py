from abc import ABC, abstractmethod

from ....Driver.Tools.AbstractClasses import BackendABC


class InterfaceABC(ABC):
    def __init__(self, BackendInstance: BackendABC,CustomErrorHandling: bool):
        self.BackendInstance: BackendABC = BackendInstance
        self.CustomErrorHandling: bool = CustomErrorHandling

    @abstractmethod
    def Initialize(self):
        ...

    @abstractmethod
    def Deinitialize(self):
        ...
