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

    @abstractmethod
    def Reserve(self, UniqueIdentifier: str) -> Lid:
        ...

    @abstractmethod
    def PreTransportCheck(self, UniqueIndentifier: str):
        ...

    @abstractmethod
    def Release(self, UniqueIdentifier: str):
        ...
