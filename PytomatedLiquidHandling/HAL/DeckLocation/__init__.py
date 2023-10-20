from . import Base
from .DeckLocation import DeckLocation

__Objects: dict[str, Base.DeckLocationABC] = dict()


def GetObjects() -> dict[str, Base.DeckLocationABC]:
    return __Objects
