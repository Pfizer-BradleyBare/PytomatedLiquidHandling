from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from PytomatedLiquidHandling.Tools.AbstractClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)

if TYPE_CHECKING:
    from ...Method.Step import TaskABC
    from ..Orchastrator import Orchastrator

import time


@dataclass
class RecurringNotification:
    OrchastratorInstance: Orchastrator
    Notifications: UniqueObjectTrackerABC[_RecurringNotification] = field(
        init=False, default_factory=UniqueObjectTrackerABC
    )

    @dataclass
    class _RecurringNotification(UniqueObjectABC):
        Message: str

        CycleTime: int
        StartTime: int = field(init=False)
        TaskInstance: TaskABC
        AcknowledgedNotification: bool = field(init=False, default=False)

        def __post_init__(self):
            self.StartTime = int(time.monotonic())

        def GetRemainingTime(self) -> int:
            return self.StartTime + self.CycleTime - int(time.monotonic())

        def IsExpired(self) -> bool:
            return self.GetRemainingTime() <= 0

        def IsAcknowledged(self) -> bool:
            Test = self.AcknowledgedNotification == True

            if Test == True:
                self.TaskInstance.ExecutionTime = int(time.monotonic()) - self.StartTime

            return Test

        def Acknowledge(self):
            self.AcknowledgedNotification = True

    def StartRecurringNotification(
        self,
        TaskInstance: TaskABC,
        Message: str,
        CycleTime: int,
    ):
        Instance = self._RecurringNotification(
            TaskInstance.UniqueIdentifier, Message, CycleTime, TaskInstance
        )

        self.Notifications.LoadSingle(Instance)

    def GetRecurringNotification(self, UniqueIdentifier: str) -> _RecurringNotification:
        return self.Notifications.GetObjectByName(UniqueIdentifier)

    def GetAcknowledgedNotifications(self) -> list[_RecurringNotification]:
        Acknowledged = list()

        for Instance in self.Notifications.GetObjectsAsList():
            if Instance.IsAcknowledged():
                Acknowledged.append(Instance)
                self.Notifications.UnloadSingle(Instance)

        return Acknowledged
