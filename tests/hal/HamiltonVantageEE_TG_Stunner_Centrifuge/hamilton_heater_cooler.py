from __future__ import annotations

import os

from loguru import logger

from plh import api, hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

labware_type = hal.labware.devices["Hamilton1500uLFlipTubeRack"]

print(
    [
        [item.layout_item.identifier for item in sub]
        for sub in api.load.group([labware_type] * 2)
    ]
)

input("ENTER")
