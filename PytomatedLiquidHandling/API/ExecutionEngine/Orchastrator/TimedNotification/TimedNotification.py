from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

if TYPE_CHECKING:
    from ...Method.Step import TaskABC
import time
from threading import Event, Thread
from PytomatedLiquidHandling.HAL import Notify


@dataclass
class TimedNotification(UniqueObjectABC):
    Message: str

    AcknowledgedNotification: bool = field(init=False, default=False)
    CycleTime: int
    StartTime: int = field(init=False)
    TaskInstance: TaskABC
    NotifyTrackerInstance: Notify.NotifyTracker

    __NotificationThreadRunnerFlag: Event = field(init=False, default=Event())

    def __post_init__(self):
        self.StartTime = int(time.monotonic())

        self.__NotificationThreadRunnerFlag.clear()

        Thread(
            name="Notification message cycle thread runner-> "
            + str(self.UniqueIdentifier),
            target=self.__NotificationThreadRunner,
        ).start()

    def IsAcknowledged(self) -> bool:
        Test = self.AcknowledgedNotification == True

        if Test == True:
            self.__NotificationThreadRunnerFlag.set()
            self.TaskInstance.ExecutionTime = int(time.monotonic()) - self.StartTime

        return Test

    def Acknowledge(self):
        self.AcknowledgedNotification = True

    def __NotificationThreadRunner(self):
        Thread(
            name="Notification message cycle thread ->  " + str(self.UniqueIdentifier),
            target=self.__RunNotificationCycle,
            daemon=True,
        ).start()

        self.__NotificationThreadRunnerFlag.wait()

    def __RunNotificationCycle(self):
        ...
