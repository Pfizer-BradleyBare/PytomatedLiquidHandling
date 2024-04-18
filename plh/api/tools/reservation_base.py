from __future__ import annotations

from dataclasses import dataclass
from typing import DefaultDict

from plh.hal.tools import HALDevice

from .loaded_labware import LoadedLabware

hal_device_reservation_tracker: dict[HALDevice, ReservationBase] = {}
"""Convienence method to get a reservation from a hal device"""

loaded_labware_reservation_tracker: dict[LoadedLabware, set[ReservationBase]] = (
    DefaultDict(set)
)
"""Conviencence method to get all reservations for a loaded labware."""


@dataclass(frozen=True)
class ReservationBase:
    hal_device: HALDevice

    loaded_labware: LoadedLabware


def reserve(reservation: ReservationBase) -> None:
    """Utility method to register a reservation."""
    hal_device_reservation_tracker[reservation.hal_device] = reservation
    loaded_labware_reservation_tracker[reservation.loaded_labware].add(reservation)


def release(reservation: ReservationBase) -> None:
    """Utility method to remove a reservation registration."""
    del hal_device_reservation_tracker[reservation.hal_device]

    loaded_labware_reservation_tracker[reservation.loaded_labware].remove(reservation)

    if len(loaded_labware_reservation_tracker[reservation.loaded_labware]) == 0:
        del loaded_labware_reservation_tracker[reservation.loaded_labware]
