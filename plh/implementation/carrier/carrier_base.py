from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, dataclasses

from plh.implementation import deck
from plh.implementation.tools import Interface, Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class CarrierBase(Resource, Interface):
    """A physical carrier on a system deck."""

    identifier: str = "None"
    """It is optional to specify an identifier. If one is not specified then the identifier will be automatically generated."""

    deck: Annotated[
        deck.DeckBase,
        BeforeValidator(deck.validate_instance),
    ]
    """A deck object."""

    num_labware_positions: int
    """Number of labware supported by the carrier."""
