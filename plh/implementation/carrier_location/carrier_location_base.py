from __future__ import annotations

from typing import Annotated

from pydantic import (
    BeforeValidator,
    dataclasses,
    model_validator,
)

from plh.implementation import carrier
from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class CarrierLocationBase(Resource):
    """A specific location on an automation deck."""

    identifier: str = "None"
    """It is optional to specify an identifier. If an identifier is not specified then identifier will be ```<carrier_config.carrier.identifier>_Pos<self.position```"""

    carrier: Annotated[
        carrier.CarrierBase,
        BeforeValidator(carrier.validate_instance),
    ]
    """A carrier object."""

    position: int
    """A position on the above carrier object."""

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: CarrierLocationBase) -> CarrierLocationBase:
        if v.identifier == "None":
            v.identifier = f"{v.carrier.identifier}_Pos{v.position!s}"
        return v
