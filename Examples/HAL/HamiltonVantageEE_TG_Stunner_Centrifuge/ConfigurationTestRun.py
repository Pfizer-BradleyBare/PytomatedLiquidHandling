import os

import yaml
from loguru import logger

from PytomatedLiquidHandling import HAL, Driver

logger.enable("PytomatedLiquidHandling")

HAL.LoadYamlConfiguration(os.path.join(os.path.dirname(__file__), "Config"))
