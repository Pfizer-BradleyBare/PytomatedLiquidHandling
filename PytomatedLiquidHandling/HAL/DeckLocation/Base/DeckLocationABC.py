from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice

from .CarrierConfig import CarrierConfig
from .TransportConfig import TransportConfig


class DeckLocationABC(HALDevice):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
        TransportConfig: See DeckLocation.Base.TransportConfig class.
    """

    CarrierConfig: CarrierConfig
    TransportConfig: TransportConfig
