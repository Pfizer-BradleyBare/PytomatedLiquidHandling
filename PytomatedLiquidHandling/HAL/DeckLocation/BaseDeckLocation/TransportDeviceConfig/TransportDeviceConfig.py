from .....Tools.AbstractClasses import UniqueObjectABC
from dataclasses import dataclass, field


@dataclass
class TransportDeviceConfig(UniqueObjectABC):
    HomeGetConfig: dict
    HomePlaceConfig: dict
    AwayGetConfig: dict
    AwayPlaceConfig: dict
