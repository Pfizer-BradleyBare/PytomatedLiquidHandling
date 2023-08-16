from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.API.Tools.Container import Container


@dataclass
class Options(OptionsABC):
    SourceContainerInstance: Container
    SourceWell: int
    DestinationContainerInstance: Container
    DestinationWell: int

    Volume: float
