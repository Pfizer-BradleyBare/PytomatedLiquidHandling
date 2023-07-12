from PytomatedLiquidHandling.HAL import DeckLocation, TempControlDevice

from ....Tools.AbstractClasses import UniqueObjectTrackerABC


class ResourceReservationTracker(
    UniqueObjectTrackerABC[
        DeckLocation.BaseDeckLocation.DeckLocationABC
        | TempControlDevice.BaseTempControlDevice.TempControlDevice
    ]
):
    pass
