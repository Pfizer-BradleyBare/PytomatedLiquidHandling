from typing import Callable, Generic, TypeVar

ExecuteReturnType = TypeVar("ExecuteReturnType")


class InterfaceCommandWithListedOptionsABC(Generic[ExecuteReturnType]):
    def __init__(
        self,
        ExecuteFunction: Callable,
        ExecutionTimeFunction: Callable,
    ):
        self.Execute: Callable[[list], ExecuteReturnType] = ExecuteFunction
        self.ExecutionTime: Callable[[list], float] = ExecutionTimeFunction

    def __call__(self, Options: list) -> ExecuteReturnType:
        return self.Execute(Options)
