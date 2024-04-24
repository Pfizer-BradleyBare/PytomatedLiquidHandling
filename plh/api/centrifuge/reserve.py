from __future__ import annotations

from plh.api import container
from plh.api.tools.loaded_labware import well_assignment_tracker
from plh.api.tools.reservation import hal_device_reservation_tracker, register

from .get_compatible_devices import get_compatible_devices
from .reservation import CentrifugeReservation


def reserve(
    g_force: float,
    *wells: container.Well,
) -> list[CentrifugeReservation]:
    """Reserve an available centrifuge device."""
    loaded_labwares = {
        loaded_labware
        for well in wells
        for loaded_labware in well_assignment_tracker[well]
    }
    # all the labware we need to reserve for. Each labware needs a reservation.

    labware = list(
        {loaded_labware.layout_item.labware for loaded_labware in loaded_labwares}
    )

    if len(labware) != 1:
        raise ValueError("Centrifuges can only spin a single labware type at a time.")

    possible_devices = get_compatible_devices(
        g_force,
        len(loaded_labwares),
        labware[0],
    )

    possible_devices = [
        device
        for device in possible_devices
        if device not in hal_device_reservation_tracker
    ]

    if len(loaded_labwares) > len(possible_devices):
        raise RuntimeError(
            "Not enough devices available for this container...",
        )

    reservations: list[CentrifugeReservation] = []
    for loaded_labware in loaded_labwares:
        device = possible_devices.pop(0)

        device.set_temperature(temperature)

        reservation = IncubateReservation(device, loaded_labware, temperature, rpm)

        register(reservation)
        reservations.append(reservation)

    return reservations
