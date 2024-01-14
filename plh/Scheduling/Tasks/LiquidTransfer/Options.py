from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsBase


@dataclass
class Options(OptionsBase):
    SourceContainerInstance: Container
    SourceWell: int
    DestinationContainerInstance: Container
    DestinationWell: int

    Volume: float
