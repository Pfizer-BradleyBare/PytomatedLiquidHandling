from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Type

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .TaskABC import TaskABC


@dataclass
class StepABC(UniqueObjectABC):
    TaskClasses: list[Type[TaskABC]] = field(init=False, default_factory=list)

    @abstractmethod
    def __post_init__(self):
        """Build the list of task classes to execute here. Note that tasks are allowed to occur more than once if needed"""
        ...
