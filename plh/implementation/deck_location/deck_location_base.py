from __future__ import annotations

from typing import Annotated, cast

from pydantic import (
    BeforeValidator,
    ValidationInfo,
    dataclasses,
    field_validator,
    model_validator,
)

from plh.implementation import carrier
from plh.implementation.tools import Resource

_used_carriers: list[str] = []


@dataclasses.dataclass(kw_only=True, eq=False)
class DeckLocationBase(Resource):
    """A specific location on an automation deck."""

    identifier: str = "None"
    """It is optional to specify an identifier. If an identifier is not specified then identifier will be ```<carrier_config.carrier.identifier>_Pos<carrier_config.position```"""

    carrier: Annotated[
        carrier.CarrierBase,
        BeforeValidator(carrier.validate_instance),
    ]
    """A carrier object."""

    position: int
    """A position on the above carrier object."""

    @field_validator("Position", mode="after")
    @classmethod
    def __position_validate(
        cls: type[DeckLocationBase],
        v: int,
        info: ValidationInfo,
    ) -> int:
        try:
            assigned_carrier = cast(carrier.CarrierBase, info.data["Carrier"])
        except KeyError:
            return v

        num_positions = assigned_carrier.num_labware_positions

        if v > num_positions:
            msg = f"Carrier position ({v!s}) must be less than total number of supported labware positions ({num_positions!s})."
            raise ValueError(msg)

        carrier_pos_id = assigned_carrier.identifier + str(v)

        if carrier_pos_id in _used_carriers:
            msg = f'Position {v!s} has already been assigned on carrier "{assigned_carrier.identifier}".'
            raise ValueError(msg)

        _used_carriers.append(carrier_pos_id)

        return v

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: DeckLocationBase) -> DeckLocationBase:
        if v.identifier == "None":
            v.identifier = f"{v.carrier.identifier}_Pos{v.position!s}"
        return v
