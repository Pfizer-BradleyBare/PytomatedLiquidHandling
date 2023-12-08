import os

import yaml

from PytomatedLiquidHandling import HAL

from loguru import logger

logger.enable("PytomatedLiquidHandling")

HAL.LoadYamlConfiguration(os.path.dirname(__file__))
