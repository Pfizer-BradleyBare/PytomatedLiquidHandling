from abc import ABC
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from ..InterfaceCommand import InterfaceCommandABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool

    class Initialize(InterfaceCommandABC[None]):
        @staticmethod
        def Execute(InterfaceHandle) -> None:
            if not isinstance(InterfaceHandle, InterfaceABC):
                raise Exception("Should never happen")

            InterfaceHandle.BackendInstance.StartBackend()

        @staticmethod
        def ExecutionTime() -> float:
            return 0

    class Deinitialize(InterfaceCommandABC[None]):
        @staticmethod
        def Execute(InterfaceHandle) -> None:
            if not isinstance(InterfaceHandle, InterfaceABC):
                raise Exception("Should never happen")

            InterfaceHandle.BackendInstance.StopBackend()

        @staticmethod
        def ExecutionTime() -> float:
            return 0
