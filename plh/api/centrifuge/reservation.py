from dataclasses import dataclass

from plh.api.tools.reservation import ReservationBase
from plh.implementation.centrifuge import CentrifugeBase


@dataclass(frozen=True)
class CentrifugeReservation(ReservationBase):
    hal_device: CentrifugeBase
    g_force: float
