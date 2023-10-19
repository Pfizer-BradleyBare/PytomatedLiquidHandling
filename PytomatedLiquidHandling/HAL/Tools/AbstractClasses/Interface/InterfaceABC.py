from abc import ABC, abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC, OptionsABC


@dataclass
class InterfaceABC(ABC):
    Backend: BackendABC
    CustomErrorHandling: bool

    def Initialize(self):
        self.Backend.StartBackend()

    def Deinitialize(self):
        self.Backend.StopBackend()
