from abc import abstractmethod
from dataclasses import dataclass, field
from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import Lid, LayoutItemTracker
from .LidReservation import LidReservationTracker


@dataclass
class LidStorage(UniqueObjectABC):
    ReservableLidTrackerInstance: LayoutItemTracker
    LidReservationTrackerInstance: LidReservationTracker = field(
        init=False, default=LidReservationTracker()
    )

    def CheckReservationExists(self, UniqueIdentifier: str) -> bool:
        try:
            self.LidReservationTrackerInstance.GetObjectByName(UniqueIdentifier)
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
