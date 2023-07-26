from dataclasses import dataclass
from typing import Any, Generic, TypeVar, Callable

ExecuteReturnType = TypeVar("ExecuteReturnType")


@dataclass(frozen=True, kw_only=True)
class InterfaceCommandABC(Generic[ExecuteReturnType]):
    Execute: Callable[[], ExecuteReturnType]
    ExecutionTime: Callable[[], float]

    def __call__(self):
        self.Execute()
