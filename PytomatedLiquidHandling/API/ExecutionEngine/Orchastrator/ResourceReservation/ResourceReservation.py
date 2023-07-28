from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import DeckLocation, TempControlDevice
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class ResourceReservation(UniqueObjectABC):
    UniqueObjectInstance: TempControlDevice.BaseTempControlDevice.TempControlDevice | DeckLocation.BaseDeckLocation.DeckLocationABC
    Flexible: bool
