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
        (1, pipette_tip),
        (2, pipette_tip),
        (3, pipette_tip),
        (4, pipette_tip),
        (5, pipette_tip),
        (6, pipette_tip),
        (7, pipette_tip),
        (8, pipette_tip),
    ],
)
input("enter")

pipette._eject(
    [
        (1, ("VStarWaste_16Pos_0001", "1")),
        (2, ("VStarWaste_16Pos_0001", "2")),
        (3, ("VStarWaste_16Pos_0001", "3")),
        (4, ("VStarWaste_16Pos_0001", "4")),
        (5, ("VStarWaste_16Pos_0001", "1")),
        (6, ("VStarWaste_16Pos_0001", "2")),
        (7, ("VStarWaste_16Pos_0001", "3")),
        (8, ("VStarWaste_16Pos_0001", "4")),
    ],
)

pipette.deinitialize()

tip.deinitialize()

hamilton_backend.stop()
