from __future__ import annotations

from dataclasses import dataclass

from plh.hal.exceptions import HALError

from .deck_location_base import DeckLocationBase
from .transportable_deck_location import TransportableDeckLocation


@dataclass
class DeckLocationNotSupportedError(HALError):
    """HAL device does not support your DeckLocation.
    This can be thrown for any LayoutItem inputs.
    """

    deck_locations: list[DeckLocationBase]
    """List of DeckLocationBase objects that were not supported."""

    def __str__(self) -> str:
        return ", ".join(
            [deck_location.identifier for deck_location in self.deck_locations],
        )


@dataclass
class DeckLocationNotTransportableError(HALError):
    """Your deck location is not transportable but the action you attempted requires a transportable deck location."""

    deck_locations: list[DeckLocationBase]
    """List of DeckLocationBase objects that were not transportable."""

    def __str__(self) -> str:
        return ", ".join(
            [deck_location.identifier for deck_location in self.deck_locations],
        )


@dataclass
class DeckLocationTransportConfigsNotCompatibleError(HALError):
    """The two transportable deck locations do not have compatible transport options.
    Thus, you cannot transport to/from these deck locations.
    You should find an intermediate deck location to enable comaptibility.
    """

    source_deck_location: TransportableDeckLocation
    """Source transportable deck location."""

    destination_deck_location: TransportableDeckLocation
    """Destination transportable deck location."""

    def __str__(self) -> str:
        return f"{self.source_deck_location.identifier} != {self.destination_deck_location.identifier}"
