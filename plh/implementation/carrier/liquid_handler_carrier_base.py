from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses, model_validator

from plh.implementation import deck

from .carrier_base import CarrierBase


@dataclasses.dataclass(kw_only=True, eq=False)
class LiquidHandlerCarrierBase(CarrierBase):
    """A physical carrier on an liquid handler system deck."""

    deck: Annotated[
        deck.LiquidHandlerDeckBase,
        BeforeValidator(deck.validate_instance),
    ]
    """A deck object."""

    track_start: int
    """The deck track where the carrier starts (Starting contact point)."""

    width: int
    """The number of tracks occupied by the carrier"""

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: LiquidHandlerCarrierBase) -> LiquidHandlerCarrierBase:
        if v.identifier == "None":
            v.identifier = f"{v.deck.identifier}_Carrier{v.track_start}"
        return v
