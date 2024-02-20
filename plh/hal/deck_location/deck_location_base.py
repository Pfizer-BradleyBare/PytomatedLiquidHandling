from __future__ import annotations

from pydantic import dataclasses, model_validator

from plh.hal.tools import HALDevice

from .carrier_config import *
from .carrier_config import CarrierConfig


@dataclasses.dataclass(kw_only=True, eq=False)
class DeckLocationBase(HALDevice):
    """A specific location on an automation deck."""

    identifier: str = "None"
    """It is optional to specify an identifier. If an identifier is not specified then identifier will be ```<carrier_config.carrier.identifier>_Pos<carrier_config.position```"""

    carrier_config: CarrierConfig
    """Carrier association for the deck location."""

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: DeckLocationBase) -> DeckLocationBase:
        if v.identifier == "None":
            v.identifier = f"{v.carrier_config.carrier.identifier}_Pos{v.carrier_config.position!s}"
        return v
