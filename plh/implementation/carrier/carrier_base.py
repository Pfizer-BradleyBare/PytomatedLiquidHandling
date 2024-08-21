from __future__ import annotations

from pydantic import dataclasses, model_validator

from plh.implementation.tools import GenericResource


@dataclasses.dataclass(kw_only=True, eq=False)
class CarrierBase(GenericResource):
    """A physical carrier on an automation system deck."""

    identifier: str = "None"
    """It is optional to specify an identifier. If one is not specified then the identifier will be ```Carrier_<track_start>```"""

    track_start: int
    """The deck track where the carrier starts (Starting contact point)."""

    width: int
    """The number of tracks occupied by the carrier"""

    num_labware_positions: int
    """Number of labware supported by the carrier."""

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: CarrierBase) -> CarrierBase:
        if v.identifier == "None":
            v.identifier = f"Carrier{v.track_start}"
        return v
