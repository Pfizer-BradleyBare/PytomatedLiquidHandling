import os
from loguru import logger
import yaml

from PytomatedLiquidHandling import HAL, Driver

logger.enable("PytomatedLiquidHandling")

HAL.LoadYamlConfiguration(os.path.dirname(__file__))
