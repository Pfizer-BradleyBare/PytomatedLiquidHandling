from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

li = hal.layout_item.devices["Carrier41_Pos1_Hamilton1500uLFlipTubeCarrier"]

vm = hal.volume_measure.devices["Pipette Measure"]

print(vm.measure_volume((li, 28), (li, 29), (li, 30), (li, 31), (li, 32)))
