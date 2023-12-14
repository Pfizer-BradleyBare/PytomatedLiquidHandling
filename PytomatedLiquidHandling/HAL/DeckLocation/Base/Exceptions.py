from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .DeckLocationABC import DeckLocationABC
    from .TransportConfig import TransportConfig


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


@dataclass
class DeckLocationTransportConfigsNotCompatible(Exception):
    SourceDeckLocation: DeckLocationABC
    DestinationDeckLocation: DeckLocationABC
    SourceTransportConfigs: list[TransportConfig] = field(
        init=False, default_factory=list
    )
    DestinationTransportConfigs: list[TransportConfig] = field(
        init=False, default_factory=list
    )

    def __post_init__(self):
        if hasattr(self.SourceDeckLocation, "TransportConfigs"):
            self.SourceTransportConfigs = getattr(
                self.SourceDeckLocation, "TransportConfigs"
            )
        if hasattr(self.DestinationDeckLocation, "TransportConfigs"):
            self.DestinationTransportConfigs = getattr(
                self.DestinationDeckLocation, "TransportConfigs"
            )
