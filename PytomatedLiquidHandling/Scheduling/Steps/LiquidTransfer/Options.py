from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.API.Tools.Container import Container


@dataclass
class Options(OptionsABC):
    SourceContainer: Container
    SourceWell: int
    DestinationContainer: Container
    DesintationWell: int
    Volume: float
    AspirateMixCycles: int
    DispenseMixCycles: int
