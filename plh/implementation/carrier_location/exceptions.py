from __future__ import annotations

from dataclasses import dataclass

from plh.implementation.exceptions import HALError

from .carrier_location_base import DeckLocationBase


@dataclass
class DeckLocationNotSupportedError(HALError):
    """HAL device does not support your DeckLocation.
    This can be thrown for any LayoutItem inputs.
    """

    deck_location: DeckLocationBase
    """DeckLocationBase object that is not supported."""

    def __str__(self) -> str:
        return self.deck_location.identifier


@dataclass
class DeckLocationNotTransportableError(HALError):
    """Your deck location is not transportable but the action you attempted requires a transportable deck location."""

    deck_location: DeckLocationBase
    """DeckLocationBase object that is not transportable."""

    def __str__(self) -> str:
        return self.deck_location.identifier


@dataclass
class DeckLocationTransportConfigsNotCompatibleError(HALError):
    """The two transportable deck locations do not have compatible transport options.
    Thus, you cannot transport to/from these deck locations.
    You should find an intermediate deck location to enable comaptibility.
    """

    source_deck_location: DeckLocationBase
    """Source transportable deck location."""

    destination_deck_location: DeckLocationBase
    """Destination transportable deck location."""

    def __str__(self) -> str:
        return f"{self.source_deck_location.identifier} != {self.destination_deck_location.identifier}"
