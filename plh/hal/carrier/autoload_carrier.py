from pydantic import dataclasses

from .carrier_base import *
from .moveable_carrier import MoveableCarrier


@dataclasses.dataclass(kw_only=True)
class AutoloadCarrier(MoveableCarrier):
    """A carrier which can be accessed and moved by a barcode reader (autoload for Hamilton systems)."""

    carrier_labware_id: str
    """The labware ID of the carrier."""
