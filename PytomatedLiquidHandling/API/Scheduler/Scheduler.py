from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ..Tools import ResourceReservation
from .Method import MethodABC, MethodTracker


@dataclass
class Scheduler(UniqueObjectTrackerABC[MethodABC]):
    LoggerInstance: Logger
    HALInstance: HAL.HAL

    MethodTrackerInstance: MethodTracker = field(init=False, default=MethodTracker())
    CompletedMethodTrackerInstance: MethodTracker = field(
        init=False, default=MethodTracker()
    )

    LoadedLayoutItems: HAL.LayoutItem.LayoutItemTracker = field(
        init=False, default=HAL.LayoutItem.LayoutItemTracker()
    )
    InUseLoadedLayoutItems: HAL.LayoutItem.LayoutItemTracker = field(
        init=False, default=HAL.LayoutItem.LayoutItemTracker()
    )

    ResourceReservationTrackerInstance: ResourceReservation.ResourceReservationTracker = field(
        init=False, default=ResourceReservation.ResourceReservationTracker()
    )

    def QueueMethod(self):
        ...
