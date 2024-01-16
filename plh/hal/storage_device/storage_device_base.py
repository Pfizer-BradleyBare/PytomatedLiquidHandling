from __future__ import annotations

from abc import abstractmethod
from dataclasses import field

from pydantic import dataclasses, field_validator

from plh.hal import layout_item as li
from plh.hal.tools import HALDevice

from .reservation import Reservation


@dataclasses.dataclass(kw_only=True)
class StorageDeviceBase(HALDevice):
    layout_items: list[li.LayoutItemBase]

    reservations: dict[str, Reservation] = field(init=False, default_factory=dict)

    @field_validator("LayoutItems", mode="before")
    @classmethod
    def __supported_lis_validate(
        cls: type[StorageDeviceBase],
        v: list[str | li.LayoutItemBase],
    ) -> list[li.LayoutItemBase]:
        supported_objects = []

        objects = li.devices

        for item in v:
            if isinstance(item, li.LayoutItemBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + li.LayoutItemBase.__name__
                    + " objects.",
                )
            else:
                supported_objects.append(objects[item])

        return supported_objects

    @abstractmethod
    def reserve(
        self: StorageDeviceBase,
        reservation_id: str,
        layout_item: li.LayoutItemBase,
    ) -> None:
        ...

    @abstractmethod
    def prepare_store(self: StorageDeviceBase, reservation_id: str) -> None:
        ...

    @abstractmethod
    def store(
        self: StorageDeviceBase,
        reservation_id: str,
    ) -> li.LayoutItemBase:
        ...

    @abstractmethod
    def release(self: StorageDeviceBase, reservation_id: str) -> None:
        ...

    @abstractmethod
    def prepare_retrieve(self: StorageDeviceBase, reservation_id: str) -> None:
        ...

    @abstractmethod
    def retrieve(
        self: StorageDeviceBase,
        reservation_id: str,
    ) -> li.LayoutItemBase:
        ...
