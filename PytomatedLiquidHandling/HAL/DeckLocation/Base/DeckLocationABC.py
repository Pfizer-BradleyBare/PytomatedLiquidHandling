from pydantic import dataclasses

from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from .CarrierConfig import CarrierConfig
from .TransportConfig import TransportConfig


@dataclasses.dataclass(kw_only=True)
class DeckLocationABC(HALDevice):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """

    CarrierConfig: CarrierConfig
    TransportConfig: TransportConfig
