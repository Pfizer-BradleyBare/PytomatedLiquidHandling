from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field, dataclasses, model_validator

from plh.hal.tools import HALDevice

if TYPE_CHECKING:
    from .carrier_config import CarrierConfig


@dataclasses.dataclass(kw_only=True)
class DeckLocationBase(HALDevice):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
    """

    identifier: str = "None"

    carrier_config: CarrierConfig = Field(validation_alias="carrierconfig")

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: DeckLocationBase) -> DeckLocationBase:
        if v.identifier == "None":
            v.identifier = f"{v.carrier_config.carrier.identifier}_Pos{v.carrier_config.position!s}"
        return v
