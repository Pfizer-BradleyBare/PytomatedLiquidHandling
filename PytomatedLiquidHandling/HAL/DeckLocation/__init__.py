from . import Base
from .DeckLocation import DeckLocation

Identifier = str
Devices: dict[Identifier, Base.DeckLocationABC] = dict()
