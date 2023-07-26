from typing import Any, Callable, Generic, TypeVar

ExecuteReturnType = TypeVar("ExecuteReturnType")


class InterfaceCommandABC(Generic[ExecuteReturnType]):
    def __init__(
        self,
        ExecuteFunction: Callable[[], ExecuteReturnType],
        ExecutionTimeFunction: Callable[[], float],
    ):
        self.Execute: Callable[[], ExecuteReturnType] = ExecuteFunction
        self.ExecutionTime: Callable[[], float] = ExecutionTimeFunction

    def __call__(self) -> ExecuteReturnType:
        return self.Execute()
