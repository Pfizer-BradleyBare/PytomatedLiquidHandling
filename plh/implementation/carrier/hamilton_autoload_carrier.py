from pydantic import dataclasses

from .moveable_carrier import *
from .moveable_carrier import MoveableCarrier


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonAutoloadCarrier(MoveableCarrier):
    """A carrier which can be accessed and moved by a barcode reader (autoload for Hamilton systems)."""

    carrier_labware_id: str
    """The labware ID of the carrier."""
