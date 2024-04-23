from .reservation import IncubateReservation


def end(reservation: IncubateReservation) -> None:
    """Stop the incubation. Will NOT move the labware off the device."""
    reservation.hal_device.set_shaking_speed(0)
    reservation.hal_device.set_temperature(25)
