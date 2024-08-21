from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses, model_validator
from pydantic.functional_validators import BeforeValidator

from plh.implementation import carrier_location, labware
from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class LayoutItemBase(Resource):
    """A labware position on a deck."""

    identifier: str = "None"
    """Identifier is optional. If identifier is not specified than identifier will be ```<deck_location.identifier>_<labware.identifier>```"""

    labware_id: str
    """Labware id from the automation software for this deck position."""

    deck_location: Annotated[
        carrier_location.CarrierLocationBase,
        BeforeValidator(carrier_location.validate_instance),
    ]
    """Deck location object associated with this position. NOTE: Many layout items can be in the same deck location."""

    labware: Annotated[
        labware.LabwareBase,
        BeforeValidator(labware.validate_instance),
    ]
    """Labware type for this layout item."""

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: LayoutItemBase) -> LayoutItemBase:
        if v.identifier == "None":
            v.identifier = f"{v.deck_location.identifier}_{v.labware.identifier!s}"
        return v
