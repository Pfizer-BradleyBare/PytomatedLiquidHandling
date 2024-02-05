from pydantic import dataclasses

from .deck_location_base import *
from .deck_location_base import DeckLocationBase


@dataclasses.dataclass(kw_only=True)
class NonTransportableDeckLocation(DeckLocationBase):
    """A specific location on an automation deck that cannot be transported to/from."""
