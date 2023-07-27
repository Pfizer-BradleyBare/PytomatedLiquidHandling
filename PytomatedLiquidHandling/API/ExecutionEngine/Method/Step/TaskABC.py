from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ...Orchastrator import Orchastrator


@dataclass
class TaskABC(UniqueObjectABC):
    Simulate: bool

    class ExecutionWindows(Enum):
        Consecutive = 1  # Consequtive means the task CANNOT move.
        AsSoonAsPossible = 2  # As soon as possible means the task will be moved to the beginning of the submethod task queue

    @dataclass
    class ExecutionResource:
        ResourceNames: list[str]
        NumRequired: int

    # This is a rule for the scheduler about how tasks must be executed. If ExecutionWindow is NOT Consecutive
    # then the scheduler is free to move the task around for better scheduling.
    @abstractmethod
    def GetExecutionWindow(self) -> ExecutionWindows:
        ...

    # This indicates whether the method should be split into submethods at this task.
    # the scheduler works be scheduling a series of tasks that make up a submethod.
    # splitting a method into submethods make the workflow easier to schedule.
    # This flag can be considered optional (False) for critical method workflows but understand that
    # parallel scheduling will be nonexistant.
    @abstractmethod
    def IsSchedulingSeparator(self) -> bool:
        ...

    # resources required by the task. This can be any HAL derived object or any container.
    @abstractmethod
    def GetRequiredResources(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> list[ExecutionResource]:
        ...

    @abstractmethod
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...

    # if float("inf") then the scheduler will assume this task is never-ending.
    # This is useful for unknown duration timers, user input, and unexpected errors.
    # Post completion of "never-ending task" the min execution time should
    # be modified to reflect the total time taken.
    @abstractmethod
    def GetExecutionTime(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> float:
        ...
