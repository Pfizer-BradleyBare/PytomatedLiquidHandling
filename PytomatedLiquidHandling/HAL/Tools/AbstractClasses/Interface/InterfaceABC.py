from abc import ABC
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool

    def Initialize(self):
        self.BackendInstance.StartBackend()

    def Deinitialize(self):
        self.BackendInstance.StopBackend()
