from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any


ExecuteReturnType = TypeVar("ExecuteReturnType")


@dataclass(frozen=True, kw_only=True)
class OptionsInterfaceCommandABC(Generic[ExecuteReturnType]):
    Execute: Callable[[Any], ExecuteReturnType]
    ExecutionTime: Callable[[Any], float]

    def __call__(self, OptionsInstance: Any) -> ExecuteReturnType:
        return self.Execute(OptionsInstance)
