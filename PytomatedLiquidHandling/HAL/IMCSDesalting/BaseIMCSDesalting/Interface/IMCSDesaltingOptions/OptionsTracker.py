from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsTrackerABC

from ...IMCSTip import DesaltingTip
from .Options import Options


@dataclass
class OptionsTracker(OptionsTrackerABC[Options]):
    TipType: DesaltingTip.TipTypes
    ElutionMethod: str
