from abc import ABC, abstractmethod

from .....Driver.Tools.AbstractClasses import BackendABC


class InterfaceABC(ABC):
    def __init__(self, BackendInstance: BackendABC, CustomErrorHandling: bool):
        self.__BackendInstance: BackendABC = BackendInstance
        self.__CustomErrorHandling: bool = CustomErrorHandling

    def GetBackend(self) -> BackendABC:
        return self.__BackendInstance

    def GetErrorHandlingSetting(self) -> bool:
        return self.__CustomErrorHandling

    @abstractmethod
    def Initialize(self):
        ...

    @abstractmethod
    def Deinitialize(self):
        ...
