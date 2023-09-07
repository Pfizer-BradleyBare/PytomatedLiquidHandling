from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .Reservation import ReservationTracker


@dataclass
class StorageABC(UniqueObjectABC):
    ReservableLayoutItemTrackerInstance: LayoutItem.LayoutItemTracker
    ReservationTrackerInstance: ReservationTracker = field(
        init=False, default_factory=ReservationTracker
    )

    def CheckReservationExists(
        self, LayoutItemInstance: LayoutItem.Base.LayoutItemABC
    ) -> bool:
        try:
            self.ReservationTrackerInstance.GetObjectByName(
                LayoutItemInstance.UniqueIdentifier
            )
            return True
        except:
            return False

    @abstractmethod
    def Reserve(
        self, LayoutItemInstance: LayoutItem.Base.LayoutItemABC
    ) -> LayoutItem.Base.LayoutItemABC:
        ...

    @abstractmethod
    def PreTransportCheck(self, LayoutItemInstance: LayoutItem.Base.LayoutItemABC):
        ...

    @abstractmethod
    def Release(self, LayoutItemInstance: LayoutItem.Base.LayoutItemABC):
        ...
