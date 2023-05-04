from abc import abstractmethod

from ....Tools.AbstractClasses import NonUniqueObjectTrackerABC, UniqueObjectABC
from ...LayoutItem import Lid
from .ReservableLid import ReservableLid


class LidStorage(UniqueObjectABC, NonUniqueObjectTrackerABC[ReservableLid]):
    def __init__(
        self,
        UniqueIdentifier: str,
    ):

        self.UniqueIdentifier: str = UniqueIdentifier

    @abstractmethod
    def Reserve(self, UniqueIdentifier: str) -> Lid:
        ...

    @abstractmethod
    def Release(self, UniqueIdentifier: str):
        ...
