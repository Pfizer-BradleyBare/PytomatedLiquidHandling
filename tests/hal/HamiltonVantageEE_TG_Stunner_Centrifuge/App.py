from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("PytomatedLiquidHandling")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

FlipTubePlate = hal.layout_item.devices["Carrier42_Pos1_Hamilton1500uLFlipTubeRack"]

closeable_container_device = hal.closeable_container.devices["FlipTube"]

closeable_container_device.initialize()

open_close_options: list[hal.closeable_container.OpenCloseOptions] = []

open_close_options.append(
    hal.closeable_container.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=1),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=2),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=3),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=4),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=5),
)
open_close_options.append(
    hal.closeable_container.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=6),
)

closeable_container_device.assert_open_close_options(open_close_options)
closeable_container_device.open(open_close_options)
closeable_container_device.close(open_close_options)

closeable_container_device.deinitialize()