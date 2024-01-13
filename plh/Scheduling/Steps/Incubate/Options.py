from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    ContainerInstance: Container
    Temperature: float
    ShakingSpeed: int
    Time: float
