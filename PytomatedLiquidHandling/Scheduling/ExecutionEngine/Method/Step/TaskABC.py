from __future__ import annotations

from abc import abstractmethod
from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Self

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ...Orchastrator import Orchastrator

if TYPE_CHECKING:
    from ..Method import Method


@dataclass
class TaskABC(UniqueObjectABC):
    class ExecutionWindows(Enum):
        Consecutive = 1  # Consequtive means the task CANNOT move.
        AsSoonAsPossible = 2  # As soon as possible means the task will be moved to the beginning of the submethod task queue

    @dataclass
    class ExecutionResource:
        ResourceUniqueIdentifiers: list[str]
        NumRequired: int

    MethodInstance: Method
    ExecutionWindow: ExecutionWindows
    SchedulingSeparator: bool
    RequiredResources: list[ExecutionResource]
    ExecutionTime: int
    ExecutionStartTime: int = field(init=False, default=0)

    @abstractmethod
    def Execute(self, OrchastratorInstance: Orchastrator):
        ...
