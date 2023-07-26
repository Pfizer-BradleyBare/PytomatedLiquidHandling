from typing import Callable, Generic, TypeVar

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC

ExecuteReturnType = TypeVar("ExecuteReturnType")
OptionsType = TypeVar("OptionsType", bound=OptionsABC)


class OptionsInterfaceCommandABC(Generic[ExecuteReturnType]):
    def __init__(
        self,
        ExecuteFunction: Callable,
        ExecutionTimeFunction: Callable,
    ):
        self.Execute: Callable[[OptionsABC], ExecuteReturnType] = ExecuteFunction
        self.ExecutionTime: Callable[[OptionsABC], float] = ExecutionTimeFunction

    def __call__(self, OptionsInstance: OptionsABC) -> ExecuteReturnType:
        return self.Execute(OptionsInstance)
