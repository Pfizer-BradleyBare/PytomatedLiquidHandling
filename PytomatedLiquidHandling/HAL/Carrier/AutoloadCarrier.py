from .MoveableCarrier import MoveableCarrier

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class AutoloadCarrier(MoveableCarrier):
    """A carrier which can be accessed and moved by a barcode reader (autoload for Hamilton systems)

    Attributes:
        CarrierLabwareID: The labware ID of the carrier.
    """

    CarrierLabwareID: str
