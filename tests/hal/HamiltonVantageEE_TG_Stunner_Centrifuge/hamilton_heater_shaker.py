from __future__ import annotations

import os
from typing import cast

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

print(263.7 - 49.25 - 188)

print(
    cast(
        hal.labware.PipettableLabware,
        hal.labware.devices["Hamilton1500uLFlipTubeRack"],
    ).get_volume_from_height(-100),
)

print(
    cast(
        hal.labware.PipettableLabware,
        hal.labware.devices["Hamilton1500uLFlipTubeRack"],
    ).get_height_from_volume(1000),
)
