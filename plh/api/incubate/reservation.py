from dataclasses import dataclass, field

from plh.api.tools.reservation import ReservationBase
from plh.hal.heat_cool_shake import HeatCoolShakeBase


@dataclass(frozen=True)
class IncubateReservation(ReservationBase):
    hal_device: HeatCoolShakeBase
    status: bool = field(init=False, default=False)
    temperature: float
    rpm: int
