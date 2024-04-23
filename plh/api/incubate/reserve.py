from __future__ import annotations

from plh.api import container
from plh.api.tools.loaded_labware import well_assignment_tracker
from plh.api.tools.reservation import hal_device_reservation_tracker, register

from .get_compatible_devices import get_compatible_devices
from .reservation import IncubateReservation


def reserve(
    temperature: float,
    rpm: int,
    *wells: container.Well,
) -> list[IncubateReservation]:
    """Reserve an available heat cool shake device sorted by lowest time to temperature. Once reserved will start heating to your desired temp."""
    loaded_labwares = {
        loaded_labware
        for well in wells
        for loaded_labware in well_assignment_tracker[well]
    }
    # all the labware we need to reserve for. Each labware needs a reservation.

    possible_devices = get_compatible_devices(
        temperature,
        rpm,
        *[loaded_labware.layout_item.labware for loaded_labware in loaded_labwares],
    )

    possible_devices = [
        device
        for device in possible_devices
        if device not in hal_device_reservation_tracker
    ]

    if len(loaded_labwares) > len(possible_devices):
        raise RuntimeError(
            "Not enough HeatCoolShake devices available for this container...",
        )

    possible_devices = [
        device
        for device, time in sorted(
            [
                (device, abs(device.set_temperature_time(temperature)))
                for device in possible_devices
            ],
            key=lambda x: x[1],
        )
    ]
    # sort the devices based on lowest time to reach temp

    reservations: list[IncubateReservation] = []
    for loaded_labware in loaded_labwares:
        device = possible_devices.pop(0)

        device.set_temperature(temperature)

        reservation = IncubateReservation(device, loaded_labware, temperature, rpm)

        register(reservation)
        reservations.append(reservation)

    return reservations
