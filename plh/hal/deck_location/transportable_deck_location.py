from __future__ import annotations

from pydantic import dataclasses

from plh.driver.tools import *

from .deck_location_base import *
from .deck_location_base import DeckLocationBase
from .transport_config import TransportConfig


@dataclasses.dataclass(kw_only=True)
class TransportableDeckLocation(DeckLocationBase):
    """A specific location on an automation deck that can be transported to/from."""

    transport_configs: list[TransportConfig]
    """A list of possible ways to transport to/from this deck location."""

    @classmethod
    def get_compatible_transport_configs(
        cls: type[TransportableDeckLocation],
        *args,
    ) -> list[TransportConfig]:
        """Gets a list of compatible transport configurations for different deck locations.

        If DeckLocationNotTransportableError is thrown then your deck location is not compatible with transport.
        """
        if not len(args) > 1:
            raise ValueError("Must compare 2 or more deck_locations.")

        if not all(
            isinstance(location, TransportableDeckLocation) for location in args
        ):
            return []

        configs = [location.transport_configs for location in args]

        return list(set.intersection(*map(set, configs)))
