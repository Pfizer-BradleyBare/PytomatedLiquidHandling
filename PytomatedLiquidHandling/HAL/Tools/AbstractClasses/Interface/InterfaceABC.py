from abc import ABC
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC

from ..InterfaceCommand import InterfaceCommandABC


@dataclass
class InterfaceABC(ABC):
    BackendInstance: BackendABC
    CustomErrorHandling: bool
    Initialize: InterfaceCommandABC[None] = field(init=False)
    Deinitialize: InterfaceCommandABC[None] = field(init=False)

    def __post_init__(self):
        self.Initialize = InterfaceCommandABC(
            ExecuteFunction=self._Initialize,
            ExecutionTimeFunction=self._InitializeTime,
        )
        self.Deinitialize = InterfaceCommandABC(
            ExecuteFunction=self._Deinitialize,
            ExecutionTimeFunction=self._DeinitializeTime,
        )

    def _Initialize(self):
        self.BackendInstance.StartBackend()

    def _InitializeTime(self) -> float:
        return 0

    def _Deinitialize(self):
        self.BackendInstance.StopBackend()

    def _DeinitializeTime(self) -> float:
        return 0
