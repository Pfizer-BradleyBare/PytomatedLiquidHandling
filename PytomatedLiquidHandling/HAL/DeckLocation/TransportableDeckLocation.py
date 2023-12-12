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

    TransportConfig: TransportConfig
