from __future__ import annotations

from typing import cast

from pydantic import dataclasses

from plh.driver.tools import *

from .deck_location_base import *
from .deck_location_base import DeckLocationBase
from .transport_config import *
from .transport_config import TransportConfig


@dataclasses.dataclass(kw_only=True, eq=False)
class TransportableDeckLocation(DeckLocationBase):
    """A specific location on an automation deck that can be transported to/from."""

    transport_configs: list[TransportConfig]
    """A list of possible ways to transport to/from this deck location."""

    @classmethod
    def get_compatible_transport_configs(
        cls: type[TransportableDeckLocation],
        *args: DeckLocationBase,
    ) -> list[tuple[TransportConfig, ...]]:
        """Gets a list of compatible transport configurations for different deck locations.

        If DeckLocationNotTransportableError is thrown then your deck location is not compatible with transport.
        """
        if not len(args) > 1:
            raise ValueError("Must compare 2 or more deck_locations.")

        if not all(
            isinstance(location, TransportableDeckLocation) for location in args
        ):
            return []

        location_configs = [
            cast(TransportableDeckLocation, location).transport_configs
            for location in args
        ]

        return [
            tuple(
                [
                    config
                    for configs in location_configs
                    for config in configs
                    if config == compatible_config
                ],
            )
            for compatible_config in list(set.intersection(*map(set, location_configs)))
        ]

    # Use intersection to find the compatible configs. NOTE: the hash for transport config only depends on transport device and get_config.
    # Then use the compatible configs to contruct our tuple of location specific transport configs that are all compatible.
