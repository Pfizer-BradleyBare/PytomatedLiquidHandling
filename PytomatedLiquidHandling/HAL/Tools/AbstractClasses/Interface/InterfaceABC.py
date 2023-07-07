from abc import ABC
from dataclasses import dataclass

from .....Driver.Tools.AbstractClasses import BackendABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool

    def Initialize(self):
        if self.BackendInstance.IsRunning == False:
            self.BackendInstance.StartBackend()

    def Deinitialize(self):
        if self.BackendInstance.IsRunning == True:
            self.BackendInstance.StopBackend()
