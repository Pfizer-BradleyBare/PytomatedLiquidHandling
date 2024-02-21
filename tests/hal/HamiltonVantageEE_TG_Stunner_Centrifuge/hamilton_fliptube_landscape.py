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

open_close_options: list[hal.closeable_container.OpenCloseOptions] = []


open_close_options.append(
    hal.closeable_container.OpenCloseOptions(layout_item=flip_tube_plate, position=2),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(layout_item=flip_tube_plate, position=6),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(layout_item=flip_tube_plate, position=4),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(layout_item=flip_tube_plate, position=5),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(layout_item=flip_tube_plate, position=3),
)

closeable_container_device.assert_supported_labware([flip_tube_plate.labware])
closeable_container_device.assert_supported_deck_locations([flip_tube_plate.deck_location])
closeable_container_device.open(open_close_options)
closeable_container_device.close(open_close_options)

input("ENTER")

closeable_container_device.deinitialize()

hamilton_backend.stop()
