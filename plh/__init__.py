"""# What is Pytomated Liquid Handling (PLH)?

PLH is an abstraction layer package for automated liquid handlers.

The main feature of PLH is no compromise abstraction at the API layer: what we lack in simplicity we make up for in high level feature set.
- PLH is made of 3 layers: Driver, HAL, and API.
- Methods written using the API layer are 100% system agnostic.
- A Tools folder is provided in each layer to be used to create new drivers, devices, etc.
- Fully typed!

Please see each layer for descriptions / examples.

"""

from loguru import logger

logger.disable("PytomatedLiquidHandling")
# Programmer is excepted to enable loguru to see PLH logs
