from __future__ import annotations

from abc import abstractmethod
from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import layout_item as li
from plh.implementation.tools import GenericResource


@dataclasses.dataclass(kw_only=True)
class Reservation:
    """Information about a reservated position."""

    layout_item: li.LayoutItemBase
    """The position reserved."""

    is_stored: bool = field(init=False, default=False)
    """Is an object current in this position."""


@dataclasses.dataclass(kw_only=True, eq=False)
class StorageDeviceBase(GenericResource):
    """Can be used to store any number and any combination of labware types."""

    layout_items: Annotated[list[li.LayoutItemBase], BeforeValidator(li.validate_list)]
    """These are the positions where storage will occur."""

    reservations: dict[str, Reservation] = field(init=False, default_factory=dict)
    """Current reserved positions."""

    @abstractmethod
    def reserve(
        self: StorageDeviceBase,
        reservation_id: str,
        layout_item: li.LayoutItemBase,
    ) -> None:
        """Creates a reservation for your layout item.
        NOTE: reservation_id must be unique.
        """
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
