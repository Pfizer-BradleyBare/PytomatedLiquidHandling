from pydantic.dataclasses import dataclass

from .Base import DeckLocationABC


@dataclass
class DeckLocation(DeckLocationABC):
    ...
