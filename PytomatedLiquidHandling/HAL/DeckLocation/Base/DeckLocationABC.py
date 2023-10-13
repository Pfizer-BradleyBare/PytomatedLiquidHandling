from dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from .CarrierConfig import CarrierConfig
from .TransportConfig import TransportConfig


@dataclass
class DeckLocationABC(HALObject):
    CarrierConfig: CarrierConfig
    TransportConfig: TransportConfig


@dataclass
class DeckLocationNotSupportedError(BaseException):
    """HAL device does not support your DeckLocation.
    This can be thrown for any LayoutItem inputs.

    Attributes:
    DeckLocations: List of DeckLocationABC objects that were not supported
    """

    DeckLocations: list[DeckLocationABC]
