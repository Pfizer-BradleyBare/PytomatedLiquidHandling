from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsBase

from plh.hal import LayoutItem

from ...IMCSTip import DesaltingTip


@dataclass(kw_only=True)
class Options(OptionsBase):
    LayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate
    Position: int


@dataclass(kw_only=True)
class OptionsList(list[Options]):
    TipType: DesaltingTip.TipTypes
    ElutionMethod: str
