from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem

from ....Tools.AbstractClasses import UniqueObjectABC
from .Reservation import ReservationTracker


@dataclass
class Storage(UniqueObjectABC):
    ReservableLayoutItemTrackerInstance: LayoutItem.LayoutItemTracker
    ReservationTrackerInstance: ReservationTracker = field(
        init=False, default_factory=ReservationTracker
    )

    def CheckReservationExists(
        self, LayoutItemInstance: LayoutItem.BaseLayoutItem.LayoutItemABC
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
        self, LayoutItemInstance: LayoutItem.BaseLayoutItem.LayoutItemABC
    ) -> LayoutItem.BaseLayoutItem.LayoutItemABC:
        ...

    @abstractmethod
    def PreTransportCheck(
        self, LayoutItemInstance: LayoutItem.BaseLayoutItem.LayoutItemABC
    ):
        ...

    @abstractmethod
    def Release(self, LayoutItemInstance: LayoutItem.BaseLayoutItem.LayoutItemABC):
        ...
