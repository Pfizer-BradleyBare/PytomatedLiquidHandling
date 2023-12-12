from .Base import DeckLocationABC
from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class DeckLocation(DeckLocationABC):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """
