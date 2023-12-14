from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import dataclasses

from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from .Base.TransportConfig import TransportConfig

if TYPE_CHECKING:
    from PytomatedLiquidHandling.HAL import Transport

    # There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
    # Basically DeckLocation should not depend on Transport. So we hide the dependacy here.
    # This may be a code smell. Not sure.


@dataclasses.dataclass(kw_only=True)
class TransportableDeckLocation(HALDevice):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """

    TransportConfigs: list[TransportConfig]

    def GetTransportDevice(
        self, OtherDeckLocation: Self
    ) -> None | Transport.Base.TransportABC:
        for Config in self.TransportConfigs:
            for OtherConfig in OtherDeckLocation.TransportConfigs:
                if Config == OtherConfig:
                    return Config.TransportDevice
        return None
