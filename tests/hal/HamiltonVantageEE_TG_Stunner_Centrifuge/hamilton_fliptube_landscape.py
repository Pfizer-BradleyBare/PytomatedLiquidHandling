from __future__ import annotations

import os

from loguru import logger

from plh import implementation

logger.enable("plh")


implementation.load_yaml_configuration(
    os.path.join(os.path.dirname(__file__), "Config"),
)

hamilton_backend = implementation.backend.devices["Hamilton"]

hamilton_backend.start()

flip_tube_plate = implementation.layout_item.devices[
    "Carrier7_Pos4_Hamilton1500uLFlipTubeRack"
]

closeable_container_device = implementation.closeable_container.devices["FlipTube"]

closeable_container_device.initialize()

closeable_container_device.assert_supported_labware(flip_tube_plate.labware)
closeable_container_device.assert_supported_carrier_locations(
    flip_tube_plate.carrier_location,
)
closeable_container_device.open(
    (flip_tube_plate, 24),
    (flip_tube_plate, 23),
    (flip_tube_plate, 22),
)

closeable_container_device.close(
    (flip_tube_plate, 24),
    (flip_tube_plate, 23),
    (flip_tube_plate, 22),
)

input("ENTER")

closeable_container_device.deinitialize()

hamilton_backend.stop()
