from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import DeckLocation, TempControlDevice
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC


@dataclass
class ResourceReservationTracker(
    UniqueObjectTrackerABC[
        DeckLocation.BaseDeckLocation.DeckLocationABC
        | TempControlDevice.BaseTempControlDevice.TempControlDevice
    ]
):
    ...
