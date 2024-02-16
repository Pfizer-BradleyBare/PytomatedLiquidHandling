from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

hamilton_backend = hal.backend.devices["Hamilton"]

hamilton_backend.start()

tip = hal.tip.devices["300uL NTR"]

tip.initialize()

print(tip.remaining_tips())

try:
    tip.discard_teir()
except RuntimeError as e:
    print(e)

input("ENTER")

tip.deinitialize()

hamilton_backend.stop()
