from __future__ import annotations

from abc import abstractmethod
from dataclasses import field

from pydantic import dataclasses, field_validator

from plh.hal import layout_item as li
from plh.hal.tools import HALDevice

from .reservation import Reservation


@dataclasses.dataclass(kw_only=True)
class StorageDeviceBase(HALDevice):
    """Can be used to store any number and any combination of labware types."""

    layout_items: list[li.LayoutItemBase]
    """These are the positions where storage will occur."""

    reservations: dict[str, Reservation] = field(init=False, default_factory=dict)
    """Current reserved positions."""

    @field_validator("layout_items", mode="before")
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
        """Creates a reservation for your layout item.
        NOTE: reservation_id must be unique."""
        ...

    @abstractmethod
    def prepare_store(self: StorageDeviceBase, reservation_id: str) -> None:
        """Prepares the storage device to accept your layout item."""
        ...

    @abstractmethod
    def store(
        self: StorageDeviceBase,
        reservation_id: str,
    ) -> li.LayoutItemBase:
        """Stores your layout item."""
        ...

    @abstractmethod
    def prepare_retrieve(self: StorageDeviceBase, reservation_id: str) -> None:
        """Prepares the storage device for retreival of your layout item."""
        ...

    @abstractmethod
    def retrieve(
        self: StorageDeviceBase,
        reservation_id: str,
    ) -> li.LayoutItemBase:
        """Retrieves your layout item."""
        ...

    @abstractmethod
    def release(self: StorageDeviceBase, reservation_id: str) -> None:
        """Removes your reservation from the storage device."""
        ...
