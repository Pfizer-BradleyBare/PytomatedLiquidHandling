from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsBase


@dataclass
class Options(OptionsBase):
    ContainerInstance: Container
    Temperature: float
    ShakingSpeed: int
    Time: float
