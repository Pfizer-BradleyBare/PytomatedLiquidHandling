from pydantic import Field, dataclasses

from .moveable_carrier import MoveableCarrier


@dataclasses.dataclass(kw_only=True)
class AutoloadCarrier(MoveableCarrier):
    """A carrier which can be accessed and moved by a barcode reader (autoload for Hamilton systems)

    Attributes:
        CarrierLabwareID: The labware ID of the carrier.
    """

    carrier_labware_id: str = Field(validation_alias="carrierlabwareid")
