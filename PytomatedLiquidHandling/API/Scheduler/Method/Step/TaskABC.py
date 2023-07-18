from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Type

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import InterfaceABC
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ...Orchastrator import Orchastrator


@dataclass
class TaskABC(UniqueObjectABC):
    class ExecutionWindows(Enum):
        AsSoonAsPossible = 1
        DuringAnyTimer = 2
        DuringNearestTimer = 3
        Consecutive = 4

    SchedulingSeparator: bool
    ExecutionWindow: ExecutionWindows
    RequiredResources: list[Type[InterfaceABC] | Container]
    MinExecutionTime: float

    @abstractmethod
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
