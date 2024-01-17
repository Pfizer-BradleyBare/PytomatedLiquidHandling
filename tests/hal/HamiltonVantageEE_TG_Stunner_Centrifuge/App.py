import os

from loguru import logger
from plh import hal

logger.enable("PytomatedLiquidHandling")


hal.load_yaml_configuration(os.path.join(os.path.dirname(__file__), "Config"))

quit()

FlipTubePlate = HAL.layoutItem.Devices["Carrier42_Pos1_Hamilton1500uLFlipTubeRack"]

closeableContainerDevice = HAL.closeableContainer.Devices["FlipTube"]

closeableContainerDevice.Initialize()

opencloseOptions: list[HAL.closeableContainer.Base.opencloseOptions] = []

opencloseOptions.append(
    HAL.closeableContainer.Base.opencloseOptions(layoutItem=FlipTubePlate, Position=1),
)
opencloseOptions.append(
    HAL.closeableContainer.Base.opencloseOptions(layoutItem=FlipTubePlate, Position=2),
)
opencloseOptions.append(
    HAL.closeableContainer.Base.opencloseOptions(layoutItem=FlipTubePlate, Position=3),
)
opencloseOptions.append(
    HAL.closeableContainer.Base.opencloseOptions(layoutItem=FlipTubePlate, Position=4),
)
opencloseOptions.append(
    HAL.closeableContainer.Base.opencloseOptions(layoutItem=FlipTubePlate, Position=5),
)
opencloseOptions.append(
    HAL.closeableContainer.Base.opencloseOptions(layoutItem=FlipTubePlate, Position=6),
)

closeableContainerDevice.AssertopencloseOptions(opencloseOptions)
closeableContainerDevice.open(opencloseOptions)
closeableContainerDevice.close(opencloseOptions)

closeableContainerDevice.Deinitialize()
