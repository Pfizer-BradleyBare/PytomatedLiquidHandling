from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice

from .CarrierConfig import CarrierConfig
from .TransportConfig import TransportConfig


class DeckLocationABC(HALDevice):
    CarrierConfig: CarrierConfig
    TransportConfig: TransportConfig
