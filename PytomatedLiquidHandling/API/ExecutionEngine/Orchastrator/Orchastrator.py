from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.Logger import Logger

from .ResourceReservation import ResourceReservationTracker
from .Timer import TimerTracker


@dataclass
class Orchastrator:
    LoggerInstance: Logger
    HALInstance: HAL.HAL

    LoadedLayoutItems: HAL.LayoutItem.LayoutItemTracker = field(
        init=False, default_factory=HAL.LayoutItem.LayoutItemTracker
    )
    InUseLoadedLayoutItems: HAL.LayoutItem.LayoutItemTracker = field(
        init=False, default_factory=HAL.LayoutItem.LayoutItemTracker
    )

    ResourceReservationTrackerInstance: ResourceReservationTracker = field(
        init=False, default_factory=ResourceReservationTracker
    )
