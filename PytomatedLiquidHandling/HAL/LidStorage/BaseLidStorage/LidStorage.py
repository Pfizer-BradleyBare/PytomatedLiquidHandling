from abc import abstractmethod

from ....Tools.AbstractClasses import (
    NonUniqueObjectTrackerABC,
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)
from ...LayoutItem import Lid
from .LidReservation import LidReservation, ReservableLid


class LidStorage(UniqueObjectABC, NonUniqueObjectTrackerABC[ReservableLid]):
    def __init__(
        self,
        UniqueIdentifier: str,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.LidReservationTrackerInstance = UniqueObjectTrackerABC[LidReservation]()

    def __CheckReservationExists(self, UniqueIdentifier: str) -> bool:
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
