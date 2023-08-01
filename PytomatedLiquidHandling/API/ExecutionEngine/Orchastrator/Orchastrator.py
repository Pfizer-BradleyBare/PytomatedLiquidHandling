from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.Logger import Logger

from .LoadedLayoutItem import LoadedLayoutItemTracker
from .ResourceReservation import ResourceReservationTracker


@dataclass
class Orchastrator:
    LoggerInstance: Logger
    HALInstance: HAL.HAL

    LoadedLayoutItemTrackerInstance: LoadedLayoutItemTracker = field(
        init=False, default_factory=LoadedLayoutItemTracker
    )

    ResourceReservationTrackerInstance: ResourceReservationTracker = field(
        init=False, default_factory=ResourceReservationTracker
    )
