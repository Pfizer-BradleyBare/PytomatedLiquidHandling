from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("PytomatedLiquidHandling")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))


hamilton_backend = hal.backend.devices["Hamilton"]

hamilton_backend.start()

tip = hal.tip.devices["1000uL FTR"]

tip.initialize()

pipette = hal.pipette.devices["Pipette"]

pipette.initialize()

pipette_tip = pipette.supported_tips[0]

pipette._pickup(
    [
        pipette_tip,
        pipette_tip,
        pipette_tip,
        pipette_tip,
        pipette_tip,
        pipette_tip,
        pipette_tip,
        pipette_tip,
    ],
)
input("enter")

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
