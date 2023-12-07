""" 
# What is Pytomated Liquid Handling (PLH)

PLH is an abstraction layer package for automated liquid handlers.

The main feature of PLH is no compromise abstraction at the API layer: what we lack in simplicity we make up for in high level feature set.
- PLH is made of 3 layers: Driver, HAL, and API.
- Methods written using the API layers are 100% system agnostic.
- Tools are provided are each layer to create new drivers, devices, etc.

Please see each layer for descriptions / examples.

"""

from loguru import logger

logger.disable("PytomatedLiquidHandling")
# Programmer is excepted to enable loguru to see PLH logs

from . import HAL, Driver
