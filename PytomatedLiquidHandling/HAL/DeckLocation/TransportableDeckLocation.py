from typing import Self

from pydantic import dataclasses

from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from .Base.TransportConfig import TransportConfig


@dataclasses.dataclass(kw_only=True)
class TransportableDeckLocation(HALDevice):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """

    TransportConfigs: list[TransportConfig]

    @classmethod
    def GetCompatibleTransportConfigs(
        cls, SourceDeckLocation: Self, DestinationDeckLocation: Self
    ) -> None | list[tuple[TransportConfig, TransportConfig]]:
        CompatibleConfigs = list()

        for Config in SourceDeckLocation.TransportConfigs:
            for OtherConfig in DestinationDeckLocation.TransportConfigs:
                if Config == OtherConfig:
                    CompatibleConfigs.append((Config, OtherConfig))
        if len(CompatibleConfigs) == 0:
            return None
        else:
            return CompatibleConfigs
