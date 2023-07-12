from PytomatedLiquidHandling.HAL import DeckLocation, TempControlDevice
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC


class ResourceReservationTracker(
    UniqueObjectTrackerABC[
        DeckLocation.BaseDeckLocation.DeckLocationABC
        | TempControlDevice.BaseTempControlDevice.TempControlDevice
    ]
):
    pass
