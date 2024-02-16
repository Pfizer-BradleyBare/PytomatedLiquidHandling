from __future__ import annotations

import os

from loguru import logger

from plh import hal

logger.enable("plh")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))


input("ENTER")
