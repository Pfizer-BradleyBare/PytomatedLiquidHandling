from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsTrackerABC

ExecuteReturnType = TypeVar("ExecuteReturnType")


@dataclass(kw_only=True, init=False)
class OptionsTrackerInterfaceCommandABC(Generic[ExecuteReturnType]):
    def __init__(self, ExecuteFunction: Callable, ExecutionTimeFunction: Callable):
        self.Execute: Callable[[OptionsTrackerABC], ExecuteReturnType] = ExecuteFunction
        self.ExecutionTime: Callable[[OptionsTrackerABC], float] = ExecutionTimeFunction

    def __call__(self, OptionsTrackerInstance: OptionsTrackerABC) -> ExecuteReturnType:
        return self.Execute(OptionsTrackerInstance)
