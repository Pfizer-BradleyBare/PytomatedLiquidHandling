from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools.Container import Container
from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    SourceContainer: Container
    SourceWell: int
    DestinationContainer: Container
    DesintationWell: int
    Volume: float
    AspirateMixCycles: int
    DispenseMixCycles: int
