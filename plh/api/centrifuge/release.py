from plh.api.tools.reservation import deregister

from .end import end
from .reservation import IncubateReservation


def release(reservation: IncubateReservation) -> None:
    """End the reservation."""
    end(reservation)
    deregister(reservation)
