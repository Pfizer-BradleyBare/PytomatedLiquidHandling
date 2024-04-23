from plh.api.tools.reservation import deregister

from .reservation import IncubateReservation


def release(reservations: list[IncubateReservation]) -> None:
    """End the reservation."""
    for reservation in reservations:
        if reservation.status is True:
            RuntimeError(
                "Reservation currently running. Must end first. Critical error."
            )

        deregister(reservation)
