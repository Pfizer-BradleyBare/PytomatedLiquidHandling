from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .Reservation import Reservation


@dataclass
class ReservationTracker(UniqueObjectTrackerABC[Reservation]):
    ...
