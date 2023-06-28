from abc import abstractmethod
from dataclasses import dataclass, field

from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker, Lid
from .Reservation import ReservationTracker


@dataclass
class Storage(UniqueObjectABC):
    ReservableLidTrackerInstance: LayoutItemTracker
    ReservationTrackerInstance: ReservationTracker = field(
        init=False, default=ReservationTracker()
    )

    def CheckReservationExists(self, UniqueIdentifier: str) -> bool:
        try:
            self.ReservationTrackerInstance.GetObjectByName(UniqueIdentifier)
            return True
        except:
            return False

    @abstractmethod
    def Reserve(self, UniqueIdentifier: str) -> Lid:
        ...

    @abstractmethod
    def PreTransportCheck(self, UniqueIndentifier: str):
        ...

    @abstractmethod
    def Release(self, UniqueIdentifier: str):
        ...
