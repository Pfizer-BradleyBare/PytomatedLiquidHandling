from ......Driver.Tools.AbstractClasses import OptionsTrackerABC
from .Options import Options
from ...IMCSTip import DesaltingTip
from dataclasses import dataclass


@dataclass
class OptionsTracker(OptionsTrackerABC[Options]):
    TipType: DesaltingTip.TipTypes
    ElutionMethod: str
