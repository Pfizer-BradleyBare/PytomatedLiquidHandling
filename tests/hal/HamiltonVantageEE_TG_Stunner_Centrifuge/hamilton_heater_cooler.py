from __future__ import annotations

import os

from loguru import logger

from plh import api, hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

labware_type = hal.labware.devices["Hamilton1500uLFlipTubeRack"]
other_labware_type = hal.labware.devices["Biorad200uLPCRPlate"]
print(
    [
        [(str(item.layout_item), meta) for item, meta in sub]
        for sub in api.load.group(*[labware_type] * 2, *[other_labware_type] * 5)
    ],
)

input("ENTER")
