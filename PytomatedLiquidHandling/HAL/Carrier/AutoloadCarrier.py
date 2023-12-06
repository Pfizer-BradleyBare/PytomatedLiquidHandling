from .MoveableCarrier import MoveableCarrier


class AutoloadCarrier(MoveableCarrier):
    """A carrier which can be accessed and moved by a barcode reader (autoload for Hamilton systems)

    Attributes:
        CarrierLabwareID: The labware ID of the carrier.
    """

    CarrierLabwareID: str
