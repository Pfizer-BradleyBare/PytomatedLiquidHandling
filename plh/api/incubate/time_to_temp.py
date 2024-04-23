from .reservation import IncubateReservation


def time_to_temp(reservations: list[IncubateReservation]) -> float:

    max_time = 0

    for reservation in reservations:
        time = reservation.hal_device.set_temperature_time(reservation.temperature)

        if time > max_time:
            max_time = time

    return max_time
