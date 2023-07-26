from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any

ExecuteReturnType = TypeVar("ExecuteReturnType")


@dataclass(frozen=True, kw_only=True)
class OptionsTrackerInterfaceCommandABC(Generic[ExecuteReturnType]):
    Execute: Callable[[Any], ExecuteReturnType]
    ExecutionTime: Callable[[Any], float]

    def __call__(self, OptionsTrackerInstance: Any) -> ExecuteReturnType:
        return self.Execute(OptionsTrackerInstance)
