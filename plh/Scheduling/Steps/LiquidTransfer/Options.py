from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsBase


@dataclass
class Options(OptionsBase):
    SourceContainer: Container
    SourceWell: int
    DestinationContainer: Container
    DesintationWell: int
    Volume: float
    AspirateMixCycles: int
    DispenseMixCycles: int
