from __future__ import annotations

from .reservation_base import (
    ReservationBase,
    hal_device_reservation_tracker,
    loaded_labware_reservation_tracker,
)


def register(reservation: ReservationBase) -> None:
    """Utility method to register a reservation."""
    if reservation.hal_device in hal_device_reservation_tracker:
        raise RuntimeError("HAL device already taken. Critical error.")

    hal_device_reservation_tracker[reservation.hal_device] = reservation
    loaded_labware_reservation_tracker[reservation.loaded_labware].add(reservation)
