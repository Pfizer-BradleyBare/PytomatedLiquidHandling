from dataclasses import dataclass

from ....Tools.AbstractClasses import UniqueObjectABC
from .CarrierConfig import CarrierConfig
from .TransportDeviceConfig import TransportDeviceConfig


@dataclass
class DeckLocationABC(UniqueObjectABC):
    CarrierConfigInstance: CarrierConfig
    TransportDeviceConfigInstance: TransportDeviceConfig
