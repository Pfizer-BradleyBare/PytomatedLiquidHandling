from dataclasses import dataclass
from abc import abstractmethod
from ...Orchastrator import Orchastrator
from ..Utilities import Utilities
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import InterfaceABC
from typing import Type
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger


@dataclass
class SubStepABC(UniqueObjectABC):
    IsTimed: bool
    StrictExecution: bool
    RequiredResources: list[Type[InterfaceABC]]
    MinExecutionTime: float

    def Execute(
        self,
        LoggerInstance: Logger,
        OrchastratorInstance: Orchastrator,
        UtilitiesInstance: Utilities,
    ):
        ...
