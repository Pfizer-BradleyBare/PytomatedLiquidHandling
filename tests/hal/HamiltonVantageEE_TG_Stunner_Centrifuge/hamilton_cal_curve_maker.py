from __future__ import annotations

import os
from itertools import pairwise
from typing import cast

from loguru import logger

from plh import hal

logger.enable("plh")

segment_volumes = [0, 320]
segment_points = [32]

vols = []
for points, (v1, v2) in zip(segment_points, pairwise(segment_volumes)):
    increment = (v2 - v1) / points
    vols += [int(v1 + increment * (i + 1)) for i in range(points)]

hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

pipette = hal.pipette.devices["Pipette"]

hal.pipette.TransferOptions


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
    ),
)

for tip in vm.pipette.supported_tips:
    tip.tip.deinitialize()

vm.backend.stop()
