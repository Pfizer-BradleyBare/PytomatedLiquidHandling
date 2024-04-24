from __future__ import annotations

import os

from loguru import logger

from plh import implementation

logger.enable("plh")


implementation.load_yaml_configuration(
    os.path.join(os.path.dirname(__file__), "Config")
)

hamilton_backend = implementation.backend.devices["Hamilton"]

hamilton_backend.start()

tip = implementation.tip.devices["1000uL FTR"]

tip.initialize()


tip.deinitialize()

hamilton_backend.stop()
