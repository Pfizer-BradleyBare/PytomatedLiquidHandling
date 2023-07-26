from abc import ABC
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from ..InterfaceCommand import InterfaceCommandABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool

    class InitializeCommand(InterfaceCommandABC):
        @staticmethod
        def Execute(InterfaceHandle):
            if not isinstance(InterfaceHandle, InterfaceABC):
                raise Exception("Should never happen")

            InterfaceHandle.BackendInstance.StartBackend()

        @staticmethod
        def ExecutionTime() -> float:
            return 0

    class DeinitializeCommand(InterfaceCommandABC):
        @staticmethod
        def Execute(InterfaceHandle):
            if not isinstance(InterfaceHandle, InterfaceABC):
                raise Exception("Should never happen")

            InterfaceHandle.BackendInstance.StopBackend()

        @staticmethod
        def ExecutionTime() -> float:
            return 0
