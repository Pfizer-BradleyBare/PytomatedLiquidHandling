from . import Base
from .NonTransportableDeckLocation import NonTransportableDeckLocation
from .TransportableDeckLocation import TransportableDeckLocation

Identifier = str
Devices: dict[Identifier, Base.DeckLocationABC] = dict()
