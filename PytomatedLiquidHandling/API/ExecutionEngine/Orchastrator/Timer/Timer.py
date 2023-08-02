from __future__ import annotations
from typing import TYPE_CHECKING

import time
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

if TYPE_CHECKING:
    from ...Method.Step import TaskABC


@dataclass
class Timer(UniqueObjectABC):
    WaitTime: int
    StartTime: int = field(init=False)
    Kill: bool = field(init=False, default=False)
    TaskInstance: TaskABC

    def __post_init__(self):
        self.StartTime = int(time.monotonic())

    def GetRemainingTime(self) -> int:
        return self.StartTime + self.WaitTime - int(time.monotonic())

    def IsExpired(self) -> bool:
        Test = self.GetRemainingTime() <= 0 or self.Kill == True

        if Test == True:
            self.TaskInstance.ExecutionTime = int(time.monotonic()) - self.StartTime

        return Test

    def ForceExpiration(self):
        self.Kill = True
