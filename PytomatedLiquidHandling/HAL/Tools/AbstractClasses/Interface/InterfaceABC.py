from abc import ABC, abstractmethod
from dataclasses import dataclass
from .....Driver.Tools.AbstractClasses import BackendABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool

    @abstractmethod
    def Initialize(self):
        ...

    @abstractmethod
    def Deinitialize(self):
        ...
