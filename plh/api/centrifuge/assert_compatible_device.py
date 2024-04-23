from __future__ import annotations

from plh.hal import centrifuge
from plh.hal import labware as lab


def assert_compatible_device(
    g_force: float,
    num_labware: int,
    labware: lab.LabwareBase,
) -> bool:
    """Confirm that the inputs are actually supported by at least 1 device."""
    possible_devices: list[centrifuge.CentrifugeBase] = []

    for device in centrifuge.devices.values():
        try:
            device.assert_supported_labware(labware)
        except lab.exceptions.LabwareNotSupportedError:
            continue

        try:
            device.assert_num_buckets(num_labware)
        except centrifuge.exceptions.InvalidBucketNumberError:
            continue

        try:
            device.assert_xG(g_force)
        except centrifuge.exceptions.GForceOutOfRangeError:
            continue

        possible_devices.append(device)
    # possible devices must support the temp and rpm and labware requirements of the wells.

    return len(possible_devices) != 0
