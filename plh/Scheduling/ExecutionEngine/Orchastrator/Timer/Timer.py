from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from PytomatedLiquidHandling.Tools.BaseClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)

if TYPE_CHECKING:
    from ...Method.Step import TaskABC
    from ..Orchastrator import Orchastrator


@dataclass
class Timer:
    OrcastratorInstance: Orchastrator
    Timers: UniqueObjectTrackerABC[_Timer] = field(
        init=False, default_factory=UniqueObjectTrackerABC
    )

    @dataclass
    class _Timer(UniqueObjectABC):
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

        def ExpirationWasForced(self) -> bool:
            return self.Kill

    def StartTimer(self, TaskInstance: TaskABC, WaitTime: int):
        Instance = self._Timer(TaskInstance.UniqueIdentifier, WaitTime, TaskInstance)

        self.Timers.LoadSingle(Instance)

    def GetTimer(self, UniqueIdentifier: str) -> _Timer:
        return self.Timers.GetObjectByName(UniqueIdentifier)

    def GetExpiredTimers(self) -> list[_Timer]:
        Expired = list()

        for Instance in self.Timers.GetObjectsAsList():
            if Instance.IsExpired():
                Expired.append(Instance)
                self.Timers.UnloadSingle(Instance)

        return Expired
