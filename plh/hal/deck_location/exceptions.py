from __future__ import annotations

from dataclasses import dataclass, field

from .deck_location_base import DeckLocationBase
from .transport_config import TransportConfig


@dataclass
class DeckLocationNotSupportedError(BaseException):
    """HAL device does not support your DeckLocation.
    This can be thrown for any LayoutItem inputs.

    Attributes
    ----------
    DeckLocations: List of DeckLocationBase objects that were not supported
    """

    deck_locations: list[DeckLocationBase]


@dataclass
class DeckLocationNotTransportableError(Exception):
    deck_location: DeckLocationBase


@dataclass
class DeckLocationTransportConfigsNotCompatibleError(Exception):
    source_deck_location: DeckLocationBase
    destination_deck_location: DeckLocationBase
    source_transport_configs: list[TransportConfig] = field(
        init=False,
        default_factory=list,
    )
    destination_transport_configs: list[TransportConfig] = field(
        init=False,
        default_factory=list,
    )

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
