from pydantic import dataclasses

from .MoveableCarrier import MoveableCarrier


@dataclasses.dataclass(kw_only=True)
class AutoloadCarrier(MoveableCarrier):
    """A carrier which can be accessed and moved by a barcode reader (autoload for Hamilton systems)

    Attributes:
        CarrierLabwareID: The labware ID of the carrier.
    """

    CarrierLabwareID: str
