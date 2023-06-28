from dataclasses import dataclass

from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from .Reservation import Reservation


@dataclass
class ReservationTracker(UniqueObjectTrackerABC[Reservation]):
    ...
