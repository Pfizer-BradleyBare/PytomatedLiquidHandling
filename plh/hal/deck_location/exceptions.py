from __future__ import annotations

from dataclasses import dataclass, field

from .deck_location_base import DeckLocationBase
from .transport_config import TransportConfig


@dataclass
class DeckLocationNotSupportedError(BaseException):
    """HAL device does not support your DeckLocation.
    This can be thrown for any LayoutItem inputs."""

    deck_locations: list[DeckLocationBase]
    """List of DeckLocationBase objects that were not supported."""


@dataclass
class DeckLocationNotTransportableError(Exception):
    """Your deck location is not transportable but the action you attempted requires a transportable deck location."""

    deck_location: DeckLocationBase
    """Deck location that is not transportable."""


@dataclass
class DeckLocationTransportConfigsNotCompatibleError(Exception):
    """The two transportable deck locations do not have compatible transport options.
    Thus, you cannot transport to/from these deck locations.
    You should find an intermediate deck location to enable comaptibility."""

    source_deck_location: DeckLocationBase
    """Source transportable deck location."""

    source_transport_configs: list[TransportConfig] = field(
        init=False,
        default_factory=list,
    )
    """Associated source transport configs."""

    destination_deck_location: DeckLocationBase
    """Destination transportable deck location."""

    destination_transport_configs: list[TransportConfig] = field(
        init=False,
        default_factory=list,
    )
    """Associated destination transport configs."""

    def __post_init__(self: DeckLocationTransportConfigsNotCompatibleError) -> None:
        from .transportable_deck_location import TransportableDeckLocation

        source_deck_location = self.source_deck_location
        if isinstance(source_deck_location, TransportableDeckLocation):
            self.source_transport_configs = source_deck_location.transport_configs

        destination_deck_location = self.destination_deck_location
        if isinstance(destination_deck_location, TransportableDeckLocation):
            self.destination_transport_configs = (
                destination_deck_location.transport_configs
            )
