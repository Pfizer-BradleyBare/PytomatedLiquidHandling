from __future__ import annotations

from .reservation_base import (
    ReservationBase,
    hal_device_reservation_tracker,
    loaded_labware_reservation_tracker,
)


def deregister(reservation: ReservationBase) -> None:
    """Utility method to remove a reservation registration."""
    if reservation.hal_device not in hal_device_reservation_tracker:
        raise RuntimeError("HAL device not reserved. Critical error.")

    del hal_device_reservation_tracker[reservation.hal_device]

    loaded_labware_reservation_tracker[reservation.loaded_labware].remove(reservation)

    if len(loaded_labware_reservation_tracker[reservation.loaded_labware]) == 0:
        del loaded_labware_reservation_tracker[reservation.loaded_labware]
