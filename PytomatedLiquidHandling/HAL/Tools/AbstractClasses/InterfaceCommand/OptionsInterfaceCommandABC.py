from dataclasses import dataclass
from typing import Generic, TypeVar, Callable
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC


ExecuteReturnType = TypeVar("ExecuteReturnType")
OptionsType = TypeVar("OptionsType", bound=OptionsABC)


@dataclass(frozen=True, kw_only=True)
class OptionsInterfaceCommandABC(Generic[ExecuteReturnType, OptionsType]):
    Execute: Callable[[OptionsType], ExecuteReturnType]
    ExecutionTime: Callable[[OptionsType], float]

    def __call__(self, OptionsInstance: OptionsType) -> ExecuteReturnType:
        return self.Execute(OptionsInstance)
