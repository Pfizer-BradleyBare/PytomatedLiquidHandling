from dataclasses import dataclass, field

from plh.api.tools.reservation import ReservationBase


@dataclass(frozen=True)
class IncubateReservation(ReservationBase):
    started: bool = field(init=False, default=False)
    temperature: float
    rpm: int
