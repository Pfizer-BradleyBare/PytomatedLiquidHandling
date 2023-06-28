from dataclasses import dataclass

from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem import CoverableItem, NonCoverableItem


@dataclass(kw_only=True)
class Options(OptionsABC):
    SourceLayoutItemInstance: CoverableItem | NonCoverableItem
    SourcePosition: int  # This is the well position. Not sequence position
    CurrentSourceVolume: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: CoverableItem | NonCoverableItem
    DestinationPosition: int  # This is the well position. Not sequence position
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float
