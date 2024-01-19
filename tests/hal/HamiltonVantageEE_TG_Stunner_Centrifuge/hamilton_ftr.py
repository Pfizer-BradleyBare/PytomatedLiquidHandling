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

print(tip.remaining_tips())
print(tip.remaining_tips_in_tier())
print(tip.get_tips(30))

input("ENTER")

tip.deinitialize()

hamilton_backend.stop()