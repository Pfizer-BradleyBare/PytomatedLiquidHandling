from __future__ import annotations

from pydantic import dataclasses

from plh.implementation import layout_item as li

from ..storage_device_base import Reservation, StorageDeviceBase


@dataclasses.dataclass(kw_only=True, eq=False)
class RandomAccessDeckStorage(StorageDeviceBase):
    """Random access storage device. Labware can be stored/retrieved without limitations."""

    def reserve(
        self: RandomAccessDeckStorage,
        reservation_id: str,
        layout_item: li.LayoutItemBase,
    ) -> None:
        if reservation_id in self.reservations:
            msg = "Reservation ID already exists"
            raise RuntimeError(msg)

        reserved_sites = [
            Site.layout_item.carrier_location for Site in self.reservations.values()
        ]

        reservation_labware = layout_item.labware

        free_sites = [
            site
            for site in self.layout_items
            if site.labware == reservation_labware
            and site.carrier_location not in reserved_sites
        ]
        # site must support the labware and must also not overlap with already reserved deck locations

        if len(free_sites) == 0:
            msg = "No sites available..."
            raise RuntimeError(msg)  # Could we potentially move something? Thought...

        self.reservations[reservation_id] = Reservation(layout_item=free_sites[0])

    def release(self: RandomAccessDeckStorage, reservation_id: str) -> None:
        if reservation_id not in self.reservations:
            msg = "Reservation ID does not exist."
            raise RuntimeError(msg)

        reservation = self.reservations[reservation_id]

        if reservation.is_stored is True:
            msg = "You must remove the object from storage before you can release the reservation"
            raise RuntimeError(msg)

        del self.reservations[reservation_id]

    def prepare_store(self: RandomAccessDeckStorage, reservation_id: str) -> None: ...

    def store(self: RandomAccessDeckStorage, reservation_id: str) -> li.LayoutItemBase:
        if reservation_id not in self.reservations:
            msg = "Reservation ID does not exist."
            raise RuntimeError(msg)

        reservation = self.reservations[reservation_id]

        if reservation.is_stored is True:
            msg = "Object already stored"
            raise RuntimeError(msg)

        reservation.is_stored = True

        return reservation.layout_item

    def prepare_retrieve(
        self: RandomAccessDeckStorage,
        reservation_id: str,
    ) -> None: ...

    def retrieve(
        self: RandomAccessDeckStorage,
        reservation_id: str,
    ) -> li.LayoutItemBase:
        if reservation_id not in self.reservations:
            msg = "Reservation ID does not exist."
            raise RuntimeError(msg)

        reservation = self.reservations[reservation_id]

        if reservation.is_stored is False:
            msg = "Object not yet stored"
            raise RuntimeError(msg)

        reservation.is_stored = False

        return reservation.layout_item
