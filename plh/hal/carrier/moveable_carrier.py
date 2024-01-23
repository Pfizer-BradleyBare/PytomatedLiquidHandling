from pydantic import dataclasses

from .carrier_base import *
from .carrier_base import CarrierBase


@dataclasses.dataclass(kw_only=True)
class MoveableCarrier(CarrierBase):
    """A carrier which can be accessed and moved manually."""
