from abc import ABC, abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC, OptionsABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool

    def Initialize(self):
        self.BackendInstance.StartBackend()

    def Deinitialize(self):
        self.BackendInstance.StopBackend()
