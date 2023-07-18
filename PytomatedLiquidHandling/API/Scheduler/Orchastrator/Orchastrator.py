from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL

from .ResourceReservation import ResourceReservationTracker
from .Timer import TimerTracker


@dataclass
class Orchastrator:
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

    TimerTrackerInstance: TimerTracker = field(init=False, default_factory=TimerTracker)
