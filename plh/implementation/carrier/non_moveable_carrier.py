from pydantic import dataclasses

from .carrier_base import *
from .carrier_base import CarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class NonMoveableCarrier(CarrierBase):
    """A carrier which can not be moved in any way."""