from pydantic import dataclasses

from .carrier_location_base import *
from .carrier_location_base import DeckLocationBase


@dataclasses.dataclass(kw_only=True, eq=False)
class NonTransportableDeckLocation(DeckLocationBase):
    """A specific location on an automation deck that cannot be transported to/from."""
