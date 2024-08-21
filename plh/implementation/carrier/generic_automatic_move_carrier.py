from pydantic import dataclasses

from .carrier_base import *
from .carrier_base import CarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class GenericAutomaticMoveCarrier(CarrierBase):
    """A carrier which can be accessed and moved by an autoloading mechanism."""
