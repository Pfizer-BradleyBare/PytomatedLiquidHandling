from dataclasses import dataclass, field

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Options import Options
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator.TimedNotification import (
    TimedNotification,
)


@dataclass
class Task(TaskABC):
    OptionsInstance: Options
    ExecutionTime: float = field(init=False, default=100000)
    SchedulingSeparator: bool = field(init=False, default=True)

    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        TimedNotificationInstance = TimedNotification(
            str(self.UniqueIdentifier) + "_TimedNotification",
            "Message",
            self.OptionsInstance.NotificationCycleTime,
            self,
            OrchastratorInstance.HALInstance,
        )
        OrchastratorInstance.TimedNotificationTrackerInstance.LoadSingle(
            TimedNotificationInstance
        )
