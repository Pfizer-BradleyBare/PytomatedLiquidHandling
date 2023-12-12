from pydantic import dataclasses

from .Base import DeckLocationABC


@dataclasses.dataclass(kw_only=True)
class NonTransportableDeckLocation(DeckLocationABC):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
    """
