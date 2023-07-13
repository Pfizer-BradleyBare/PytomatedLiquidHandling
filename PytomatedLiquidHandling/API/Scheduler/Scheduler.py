from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Method import MethodTracker
from .Orchastrator import Orchastrator


@dataclass
class Scheduler:
    LoggerInstance: Logger
    HALInstance: HAL.HAL
    OrchastratorInstance: Orchastrator = field(init=False)

    MethodTrackerInstance: MethodTracker = field(
        init=False, default_factory=MethodTracker
    )
    CompletedMethodTrackerInstance: MethodTracker = field(
        init=False, default_factory=MethodTracker
    )

    def __post_init__(self):
        self.OrchastratorInstance = Orchastrator(self.LoggerInstance, self.HALInstance)

    def QueueMethod(self):
        ...
