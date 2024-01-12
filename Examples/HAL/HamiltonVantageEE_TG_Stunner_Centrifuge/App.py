import os

import yaml
from loguru import logger

from PytomatedLiquidHandling import HAL

logger.enable("PytomatedLiquidHandling")

HAL.LoadYamlConfiguration(os.path.join(os.path.dirname(__file__), "Config"))

quit()

FlipTubePlate = HAL.LayoutItem.Devices["Carrier42_Pos1_Hamilton1500uLFlipTubeRack"]

CloseableContainerDevice = HAL.CloseableContainer.Devices["FlipTube"]

CloseableContainerDevice.Initialize()

OpenCloseOptions: list[HAL.CloseableContainer.Base.OpenCloseOptions] = list()

OpenCloseOptions.append(
    HAL.CloseableContainer.Base.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=1)
)
OpenCloseOptions.append(
    HAL.CloseableContainer.Base.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=2)
)
OpenCloseOptions.append(
    HAL.CloseableContainer.Base.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=3)
)
OpenCloseOptions.append(
    HAL.CloseableContainer.Base.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=4)
)
OpenCloseOptions.append(
    HAL.CloseableContainer.Base.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=5)
)
OpenCloseOptions.append(
    HAL.CloseableContainer.Base.OpenCloseOptions(LayoutItem=FlipTubePlate, Position=6)
)

CloseableContainerDevice.AssertOpenCloseOptions(OpenCloseOptions)
CloseableContainerDevice.Open(OpenCloseOptions)
CloseableContainerDevice.Close(OpenCloseOptions)

CloseableContainerDevice.Deinitialize()