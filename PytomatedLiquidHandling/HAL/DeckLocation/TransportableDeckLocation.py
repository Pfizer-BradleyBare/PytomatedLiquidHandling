from __future__ import annotations

from typing import cast

from pydantic import dataclasses


from .Base.TransportConfig import TransportConfig
from .Base import Exceptions, DeckLocationABC


@dataclasses.dataclass(kw_only=True)
class TransportableDeckLocation(DeckLocationABC):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """

    TransportConfigs: list[TransportConfig]

    @classmethod
    def GetCompatibleTransportConfigs(
        cls,
        SourceDeckLocation: DeckLocationABC,
        DestinationDeckLocation: DeckLocationABC,
    ) -> list[tuple[TransportConfig, TransportConfig]]:
        Excepts = list()

        if not isinstance(SourceDeckLocation, TransportableDeckLocation):
            Excepts.append(Exceptions.DeckLocationNotTransportable(SourceDeckLocation))

        if not isinstance(DestinationDeckLocation, TransportableDeckLocation):
            Excepts.append(
                Exceptions.DeckLocationNotTransportable(DestinationDeckLocation)
            )

        if len(Excepts) != 0:
            raise ExceptionGroup("", Excepts)

        SourceDeckLocation = cast(TransportableDeckLocation, SourceDeckLocation)
        DestinationDeckLocation = cast(
            TransportableDeckLocation, DestinationDeckLocation
        )

        CompatibleConfigs = list()

        for Config in SourceDeckLocation.TransportConfigs:
            for OtherConfig in DestinationDeckLocation.TransportConfigs:
                if Config == OtherConfig:
                    CompatibleConfigs.append((Config, OtherConfig))

        return CompatibleConfigs
