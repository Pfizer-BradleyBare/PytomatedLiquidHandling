from __future__ import annotations

from plh.api.deck_manager import move_loaded_labware

from .reservation import IncubateReservation


def start(reservations: list[IncubateReservation]) -> None:
    """Move the reservation to the reserved device then start heating and shaking at the reserved parameters."""
    loaded_labwares = [reservation.loaded_labware for reservation in reservations]

    destination_deck_locations = [
        reservation.hal_device.get_layout_item(
            reservation.loaded_labware.layout_item.labware,
        ).deck_location
        for reservation in reservations
    ]

    move_loaded_labware(loaded_labwares, destination_deck_locations)

    for reservation in reservations:

        if reservation.status is True:
            RuntimeError("Reservation already started. Critical error.")

        reservation.hal_device.set_temperature(reservation.temperature)
        reservation.hal_device.set_shaking_speed(reservation.rpm)
