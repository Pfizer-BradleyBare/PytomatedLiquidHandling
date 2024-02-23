from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

hamilton_backend = hal.backend.devices["Hamilton"]

hamilton_backend.start()

flip_tube_plate = hal.layout_item.devices["Carrier42_Pos1_Hamilton1500uLFlipTubeRack"]

closeable_container_device = hal.closeable_container.devices["FlipTube"]

closeable_container_device.initialize()

closeable_container_device.assert_supported_labware(flip_tube_plate.labware)
closeable_container_device.assert_supported_deck_locations(
    flip_tube_plate.deck_location,
)
closeable_container_device.open(
    (flip_tube_plate, 2),
    (flip_tube_plate, 6),
    (flip_tube_plate, 4),
    (flip_tube_plate, 5),
    (flip_tube_plate, 3),
)
closeable_container_device.close(
    (flip_tube_plate, 2),
    (flip_tube_plate, 6),
    (flip_tube_plate, 4),
    (flip_tube_plate, 5),
    (flip_tube_plate, 3),
)

input("ENTER")

closeable_container_device.deinitialize()

hamilton_backend.stop()
