from abc import abstractmethod

from pydantic import field_validator

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from .Reservation import Reservation

from pydantic import dataclasses
from dataclasses import field


@dataclasses.dataclass(kw_only=True)
class StorageDeviceABC(HALDevice):
    LayoutItems: list[LayoutItem.Base.LayoutItemABC]

    _Reservations: dict[str, Reservation] = field(init=False, default_factory=dict)

    @field_validator("LayoutItems", mode="before")
    def __SupportedLabwaresValidate(cls, v):
        SupportedObjects = list()

        Objects = LayoutItem.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + LayoutItem.Base.LayoutItemABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

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
