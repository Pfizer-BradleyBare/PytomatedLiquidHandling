from abc import abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Self, Type

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Orchastrator import Orchastrator
from ..Utilities import Utilities


@dataclass
class StepABC(UniqueObjectABC):
    AllStepClasses: ClassVar[list[Type[Self]]] = list()

    StepPreExecuteBlocks: list[Type[Self]] = field(init=False, default_factory=list)
    StepExecuteBlocks: list[Type[Self]] = field(init=False, default_factory=list)

    PreExecuteComplete: bool = field(init=False, default=False)
    ExecuteComplete: bool = field(init=False, default=False)

    def __init_subclass__(cls) -> None:
        StepABC.AllStepClasses.append(cls)

    @abstractmethod
    def HasTimer(self) -> bool:
        ...

    @abstractmethod
    def PreExecuteTime(self) -> float:
        ...

    def PreExecute(
        self,
        Simulate: bool,
        OrchastratorInstance: Orchastrator,
        UtilitiesInstance: Utilities,
        TimeTillExecution: float,
    ):
        self.PreExecuteComplete = True

    @abstractmethod
    def ExecuteTime(self) -> float:
        ...

    @abstractmethod
    def Execute(
        self,
        Simulate: bool,
        OrchastratorInstance: Orchastrator,
        UtilitiesInstance: Utilities,
    ):
        ...
