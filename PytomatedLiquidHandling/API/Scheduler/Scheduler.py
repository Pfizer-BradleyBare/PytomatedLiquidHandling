from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.Logger import Logger

from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from .Method import MethodABC, MethodTracker
from .ResourceReservation import ResourceReservationTracker


@dataclass
class Scheduler(UniqueObjectTrackerABC[MethodABC]):
    LoggerInstance: Logger
    HALInstance: HAL.HAL
    MethodTrackerInstance: MethodTracker = field(init=False, default=MethodTracker())
    CompletedMethodTrackerInstance: MethodTracker = field(
        init=False, default=MethodTracker()
    )
    ResourceReservationTrackerInstance: ResourceReservationTracker = field(
        init=False, default=ResourceReservationTracker()
    )

    def QueueMethod(self):
        ...
