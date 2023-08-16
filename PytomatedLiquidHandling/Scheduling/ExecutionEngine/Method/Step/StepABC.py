from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Orchastrator import Orchastrator

if TYPE_CHECKING:
    from ..Method import Method

from .TaskABC import TaskABC


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def GenerateTasks(
        self,
        MethodInstance: Method,
        OrchastratorInstance: Orchastrator,
    ) -> list[TaskABC]:
        ...
