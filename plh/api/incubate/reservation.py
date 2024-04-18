from dataclasses import dataclass, field

from plh.api.tools import ReservationBase


@dataclass(frozen=True)
class IncubateReservation(ReservationBase):
    Started: bool = field(init=False, default=False)
    Temperature: float
    RPM: int
