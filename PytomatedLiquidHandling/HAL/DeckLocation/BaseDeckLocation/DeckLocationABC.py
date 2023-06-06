from ....Tools.AbstractClasses import UniqueObjectABC
from .TransportDeviceConfig import TransportDeviceConfig
from dataclasses import dataclass


@dataclass
class DeckLocationABC(UniqueObjectABC):
    TransportDeviceConfigInstance: TransportDeviceConfig
