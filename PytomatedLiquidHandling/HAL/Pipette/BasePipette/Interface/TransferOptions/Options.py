from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import LayoutItem

from ......Driver.Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    SourceLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    SourcePosition: int  # This is the well position. Not sequence position
    CurrentSourceVolume: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    DestinationPosition: int  # This is the well position. Not sequence position
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float
