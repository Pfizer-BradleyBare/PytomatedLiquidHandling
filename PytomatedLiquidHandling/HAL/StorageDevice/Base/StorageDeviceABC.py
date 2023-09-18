from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from .Reservation import Reservation


@dataclass
class StorageDeviceABC(HALObject):
    ReservableLayoutItems: list[LayoutItem.Base.LayoutItemABC]

    Reservations: dict[str, Reservation] = field(init=False, default_factory=dict)

    @abstractmethod
    def Reserve(
        self, ReservationID: str, LayoutItemInstance: LayoutItem.Base.LayoutItemABC
    ):
        ...

    @abstractmethod
    def PrepareStore(self, ReservationID: str):
        ...

    @abstractmethod
    def Store(self, ReservationID: str) -> LayoutItem.Base.LayoutItemABC:
        ...

    @abstractmethod
    def Release(self, ReservationID: str):
        ...

    @abstractmethod
    def PrepareRetrieve(self, ReservationID: str):
        ...

    @abstractmethod
    def Retrieve(self, ReservationID: str) -> LayoutItem.Base.LayoutItemABC:
        ...
