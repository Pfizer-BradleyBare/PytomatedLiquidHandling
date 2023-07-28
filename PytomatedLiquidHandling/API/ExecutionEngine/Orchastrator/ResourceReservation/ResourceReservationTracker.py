from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .ResourceReservation import ResourceReservation


@dataclass
class ResourceReservationTracker(UniqueObjectTrackerABC[ResourceReservation]):
    ...
