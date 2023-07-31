from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    ContainerInstance: Container
    Temperature: float
    ShakingSpeed: int
    Time: float
