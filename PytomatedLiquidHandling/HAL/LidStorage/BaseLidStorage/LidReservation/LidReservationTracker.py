from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from .LidReservation import LidReservation
from dataclasses import dataclass


@dataclass
class LidReservationTracker(UniqueObjectTrackerABC[LidReservation]):
    ...
