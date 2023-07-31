from abc import abstractmethod
from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Self

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ...Orchastrator import Orchastrator


@dataclass
class TaskABC(UniqueObjectABC):
    class ExecutionWindows(Enum):
        Consecutive = 1  # Consequtive means the task CANNOT move.
        AsSoonAsPossible = 2  # As soon as possible means the task will be moved to the beginning of the submethod task queue

    @dataclass
    class ExecutionResource:
        ResourceUniqueIdentifiers: list[str]
        NumRequired: int

    Simulate: bool
    Tasks: list[Self]
    OrchastratorInstance: InitVar[Orchastrator]
    ExecutionWindow: ExecutionWindows = field(init=False)
    SchedulingSeparator: bool = field(init=False)
    RequiredResources: list[ExecutionResource] = field(init=False)

    @abstractmethod
    def __post_init__(self, OrchastratorInstance: Orchastrator):
        """Set the execution window, SchedulingSeparator, and required resources variables here. Note that these are allowed to be changed by the scheduler."""
        ...

    @abstractmethod
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...

    @abstractmethod
    def GetExecutionTime(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> float:
        ...
