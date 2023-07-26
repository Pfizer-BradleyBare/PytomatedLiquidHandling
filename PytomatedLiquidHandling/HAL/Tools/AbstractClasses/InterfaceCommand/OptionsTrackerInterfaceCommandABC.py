from dataclasses import dataclass
from typing import Generic, TypeVar, Callable
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsTrackerABC

ExecuteReturnType = TypeVar("ExecuteReturnType")
OptionsTrackerType = TypeVar("OptionsTrackerType", bound=OptionsTrackerABC)


@dataclass(frozen=True, kw_only=True)
class OptionsTrackerInterfaceCommandABC(Generic[ExecuteReturnType, OptionsTrackerType]):
    Execute: Callable[[OptionsTrackerType], ExecuteReturnType]
    ExecutionTime: Callable[[OptionsTrackerType], float]

    def __call__(self, OptionsTrackerInstance: OptionsTrackerType):
        self.Execute(OptionsTrackerInstance)
