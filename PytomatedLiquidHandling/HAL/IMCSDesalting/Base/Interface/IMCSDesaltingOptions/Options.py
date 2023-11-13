from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import LayoutItem

from ...IMCSTip import DesaltingTip


@dataclass(kw_only=True)
class Options(OptionsABC):
    LayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate
    Position: int


@dataclass(kw_only=True)
class ListedOptions(list[Options]):
    TipType: DesaltingTip.TipTypes
    ElutionMethod: str
