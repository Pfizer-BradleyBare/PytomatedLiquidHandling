from __future__ import annotations

from plh.hal import heat_cool_shake
from plh.hal import labware as lab


def assert_compatible_device(
    temperature: float,
    rpm: int,
    labware: lab.LabwareBase,
) -> bool:
    """Confirm that the temperature, shaking rpm speed, and labware is actually supported by at least 1 heat cool shake device."""
    possible_devices: list[heat_cool_shake.HeatCoolShakeBase] = []

    for device in heat_cool_shake.devices.values():
        try:
            device.assert_supported_labware(labware)
        except lab.exceptions.LabwareNotSupportedError:
            continue

        try:
            device.assert_rpm(rpm)
        except heat_cool_shake.exceptions.ShakingNotSupportedError:
            continue

        try:
            device.assert_temperature(temperature)
        except (
            heat_cool_shake.exceptions.CoolingNotSupportedError,
            heat_cool_shake.exceptions.HeatingNotSupportedError,
        ):
            continue

        possible_devices.append(device)
    # possible devices must support the temp and rpm and labware requirements of the wells.

    return len(possible_devices) != 0