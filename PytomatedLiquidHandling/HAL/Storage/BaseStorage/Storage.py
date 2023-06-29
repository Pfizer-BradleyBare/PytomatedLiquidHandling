from abc import abstractmethod
from dataclasses import dataclass, field

from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker
from ...LayoutItem.BaseLayoutItem import LayoutItemABC
from .Reservation import ReservationTracker


@dataclass
class Storage(UniqueObjectABC):
    ReservableLayoutItemTrackerInstance: LayoutItemTracker
    ReservationTrackerInstance: ReservationTracker = field(
        init=False, default=ReservationTracker()
    )

    def CheckReservationExists(self, LayoutItemInstance: LayoutItemABC) -> bool:
        try:
            self.ReservationTrackerInstance.GetObjectByName(
                LayoutItemInstance.UniqueIdentifier
            )
            return True
        except:
            return False

    @abstractmethod
    def Reserve(self, LayoutItemInstance: LayoutItemABC) -> LayoutItemABC:
        ...

    @abstractmethod
    def PreTransportCheck(self, LayoutItemInstance: LayoutItemABC):
        ...

    @abstractmethod
    def Release(self, LayoutItemInstance: LayoutItemABC):
        ...
