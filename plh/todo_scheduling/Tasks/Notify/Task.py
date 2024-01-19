from dataclasses import dataclass, field

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Scheduling.ExecutionEngine.Orchastrator.RecurringNotification import (
    TimedNotification,
)

from .options import Options


@dataclass
class Task(TaskABC):
    OptionsInstance: Options
    ExecutionTime: float = field(init=False, default=100000)
    SchedulingSeparator: bool = field(init=False, default=True)

    def Execute(self, OrchastratorInstance: Orchastrator):
        TimedNotificationInstance = TimedNotification(
            str(self.UniqueIdentifier) + "_TimedNotification",
            "Message",
            self.OptionsInstance.NotificationCycleTime,
            self,
            OrchastratorInstance.HALInstance,
        )
        OrchastratorInstance.TimedNotificationTrackerInstance.LoadSingle(
            TimedNotificationInstance,
        )
