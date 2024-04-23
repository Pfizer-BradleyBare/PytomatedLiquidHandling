from __future__ import annotations

from plh.api.deck_manager import move_loaded_labware
from plh.hal import deck_location

from .reservation import IncubateReservation


def end(
    reservations: list[IncubateReservation],
    deck_locations: list[deck_location.DeckLocationBase],
) -> None:
    """Stops the reservations. Will move the occupying labware to positions specified by deck_locations.
    NOTE: deck_locations must be greater than or equal to reservations.
    """
    if len(deck_locations) < len(reservations):
        ValueError(
            "Number of deck locations must be greater than number of reservations to successfully move labware from the device.",
        )

    for reservation in reservations:
        if reservation.status is False:
            RuntimeError("Reservation not yet started. Critical error.")

        reservation.hal_device.set_shaking_speed(0)
        reservation.hal_device.set_temperature(25)

    move_loaded_labware(
        [reservation.loaded_labware for reservation in reservations],
        deck_locations,
    )
