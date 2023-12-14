from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .DeckLocationABC import DeckLocationABC


@dataclass
class DeckLocationNotSupportedError(BaseException):
    """HAL device does not support your DeckLocation.
    This can be thrown for any LayoutItem inputs.

    Attributes:
    DeckLocations: List of DeckLocationABC objects that were not supported
    """

    DeckLocations: list[DeckLocationABC]


@dataclass
class DeckLocationNotTransportable(Exception):
    DeckLocation: DeckLocationABC
