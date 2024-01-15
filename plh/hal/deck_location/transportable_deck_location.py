from __future__ import annotations

from typing import TYPE_CHECKING, cast

from pydantic import dataclasses

from .deck_location_base import DeckLocationBase
from .exceptions import DeckLocationNotTransportableError

if TYPE_CHECKING:
    from .transport_config import TransportConfig


@dataclasses.dataclass(kw_only=True)
class TransportableDeckLocation(DeckLocationBase):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """

    transport_configs: list[TransportConfig]

    @classmethod
    def get_compatible_transport_configs(
        cls: type[TransportableDeckLocation],
        source_deck_location: DeckLocationBase,
        destination_deck_location: DeckLocationBase,
    ) -> list[tuple[TransportConfig, TransportConfig]]:
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
