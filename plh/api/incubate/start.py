from plh.api.deck_manager import move_loaded_labware

from .reservation import IncubateReservation


def start(reservation: IncubateReservation) -> None:
    """Move the reservation to the reserved device then start heating and shaking at the reserved parameters."""
    destination_deck_location = reservation.hal_device.get_layout_item(
        reservation.loaded_labware.labware,
    ).deck_location

    move_loaded_labware([reservation.loaded_labware], [destination_deck_location])

    reservation.hal_device.set_temperature(reservation.temperature)
    reservation.hal_device.set_shaking_speed(reservation.rpm)
