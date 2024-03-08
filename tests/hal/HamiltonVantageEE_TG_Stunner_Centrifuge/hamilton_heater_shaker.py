from __future__ import annotations

import os
from typing import cast

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))


print(
    cast(
        hal.labware.PipettableLabware,
        hal.labware.devices["Hamilton1500uLFlipTubeRack"],
    ).get_volume_from_height(263.7 - 188),
)


input("ENTER")
