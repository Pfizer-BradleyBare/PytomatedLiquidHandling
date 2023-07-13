from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.API.Tools import ResourceReservation
from PytomatedLiquidHandling.Tools.Logger import Logger


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

    _ResourceReservationTrackerInstance: ResourceReservation.ResourceReservationTracker = field(
        init=False, default_factory=ResourceReservation.ResourceReservationTracker
    )
