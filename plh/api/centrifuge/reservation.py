from dataclasses import dataclass

from plh.api.tools.reservation import ReservationBase
from plh.hal.heat_cool_shake import HeatCoolShakeBase


@dataclass(frozen=True)
class IncubateReservation(ReservationBase):
    hal_device: HeatCoolShakeBase
    temperature: float
    rpm: int
