from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Self, Type

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import InterfaceABC
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ...Orchastrator import Orchastrator


@dataclass
class TaskABC(UniqueObjectABC):
    class ExecutionWindows(Enum):
        Consecutive = 1  # Consequtive means the task CANNOT move.
        AsSoonAsPossible = 2  # As soon as possible means the task will be moved to the beginning of the submethod task queue

    SchedulingSeparator: bool  # This indicates whether the method should be split into submethods at this task
    ExecutionWindow: ExecutionWindows
    RequiredResources: list[Type[InterfaceABC] | Container]
    MinExecutionTime: float

    QueueUponCompletion: list[list] = field(init=False, default_factory=list)

    @abstractmethod
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
