from __future__ import annotations

from dataclasses import dataclass
from typing import DefaultDict

from plh.api.tools.loaded_labware import LoadedLabware
from plh.implementation.tools import HALDevice

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
