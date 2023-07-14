from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.Logger import Logger

from .ResourceReservation import ResourceReservationTracker


@dataclass
class Orchastrator:
    LoggerInstance: Logger
    _HALInstance: HAL.HAL

    _LoadedLayoutItems: HAL.LayoutItem.LayoutItemTracker = field(
        init=False, default_factory=HAL.LayoutItem.LayoutItemTracker
    )
    _InUseLoadedLayoutItems: HAL.LayoutItem.LayoutItemTracker = field(
        init=False, default_factory=HAL.LayoutItem.LayoutItemTracker
    )

    _ResourceReservationTrackerInstance: ResourceReservationTracker = field(
        init=False, default_factory=ResourceReservationTracker
    )
