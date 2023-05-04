from PytomatedLiquidHandling.HAL.LayoutItem import Lid

from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from ..LayoutItem import Lid
from .BaseLidStorage import LidStorage


class RandomAccessLidStorage(LidStorage):
    def __init__(
        self,
        UniqueIdentifier: str,
        AvailableLidsTrackerInstance: UniqueObjectTrackerABC[Lid],
    ):
        LidStorage.__init__(self, UniqueIdentifier, AvailableLidsTrackerInstance)

    def Reserve(self, UniqueIdentifier: str) -> Lid:
        AvailableLids = self.AvailableLidsTrackerInstance.GetObjectsAsList()

        if len(AvailableLids) != 0:
            LidInstance = AvailableLids[0]
            self.AvailableLidsTrackerInstance.ManualUnload

    def Release(self, UniqueIdentifier: str):
        return super().Release(LidInstance)
