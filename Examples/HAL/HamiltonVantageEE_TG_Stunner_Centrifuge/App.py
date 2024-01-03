import os

import yaml
from loguru import logger

from PytomatedLiquidHandling import HAL

logger.enable("PytomatedLiquidHandling")

HAL.LoadYamlConfiguration(os.path.join(os.path.dirname(__file__), "Config"))

ClosableContainerDevice = HAL.CloseableContainer.Devices["FlipTube"]
