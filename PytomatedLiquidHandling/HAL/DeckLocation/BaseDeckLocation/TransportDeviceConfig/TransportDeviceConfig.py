from dataclasses import dataclass

from .....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class TransportDeviceConfig(UniqueObjectABC):
    HomeGetConfig: dict
    HomePlaceConfig: dict
    AwayGetConfig: dict
    AwayPlaceConfig: dict
