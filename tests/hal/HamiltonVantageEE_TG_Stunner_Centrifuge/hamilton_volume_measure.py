from __future__ import annotations

import os

from loguru import logger

from plh import hal
from typing import cast

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

li = hal.layout_item.devices["Carrier41_Pos1_Hamilton1500uLFlipTubeCarrier"]

vm = cast(
    hal.container_measure.Hamilton50uLCORE8,
    hal.container_measure.devices["Pipette Measure"],
)

vm.backend.simulation_on = False
vm.backend.start()

for tip in vm.pipette.supported_tips:
    tip.tip.initialize()


print(
    vm.measure(
        (li, 32),
        (li, 31),
        (li, 30),
        (li, 29),
        (li, 28),
        (li, 27),
        (li, 26),
        (li, 25),
        (li, 24),
        (li, 23),
        (li, 22),
        (li, 21),
        (li, 20),
    )
)

for tip in vm.pipette.supported_tips:
    tip.tip.deinitialize()

vm.backend.stop()
