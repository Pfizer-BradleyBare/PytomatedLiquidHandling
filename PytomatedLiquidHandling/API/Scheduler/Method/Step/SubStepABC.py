from dataclasses import dataclass
from abc import abstractmethod
from ...Orchastrator import Orchastrator
from ..Utilities import Utilities
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import InterfaceABC
from typing import Type
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class SubStepABC(UniqueObjectABC):
    IsTimed: bool
    RequiresParentCompletion: bool

    @abstractmethod
    def GetRequiredResources(
        self, OrchastratorInstance: Orchastrator
    ) -> list[Type[InterfaceABC]]:
        ...

    @abstractmethod
    def GetExecutionTime(self) -> float:
        ...

    def Execute(self, OrchastratorInstance: Orchastrator, UtilitiesInstance: Utilities):
        ...
