from __future__ import annotations

from typing import cast

from pydantic import dataclasses

from plh.driver.tools import *

from .deck_location_base import *
from .deck_location_base import DeckLocationBase
from .exceptions import DeckLocationNotTransportableError
from .transport_config import TransportConfig


@dataclasses.dataclass(kw_only=True)
class TransportableDeckLocation(DeckLocationBase):
    """A specific location on an automation deck."""

    transport_configs: list[TransportConfig]
    """A list of possible ways to transport to/from this deck location."""

    @classmethod
    def get_compatible_transport_configs(
        cls: type[TransportableDeckLocation],
        source_deck_location: DeckLocationBase,
        destination_deck_location: DeckLocationBase,
    ) -> list[tuple[TransportConfig, TransportConfig]]:
        """Gets a list of compatible transport configurations for 2 different deck locations.
        You should call ```"""

        excepts = []

        if not isinstance(source_deck_location, TransportableDeckLocation):
            excepts.append(DeckLocationNotTransportableError(source_deck_location))

        if not isinstance(destination_deck_location, TransportableDeckLocation):
            excepts.append(
                DeckLocationNotTransportableError(destination_deck_location),
            )

        if len(excepts) != 0:
            msg = ""
            raise ExceptionGroup(msg, excepts)

        source_deck_location = cast(TransportableDeckLocation, source_deck_location)
        destination_deck_location = cast(
            TransportableDeckLocation,
            destination_deck_location,
        )

        return [
            (config, other_config)
            for config in source_deck_location.transport_configs
            for other_config in destination_deck_location.transport_configs
            if config == other_config
        ]
