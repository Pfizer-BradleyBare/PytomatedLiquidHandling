from ......Driver.Tools.AbstractClasses import OptionsABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(OptionsABC):
    SourceLayoutItemInstance: CoverablePosition | NonCoverablePosition
    SourcePosition: int  # This is the well position. Not sequence position
    CurrentSourceVolume: float
    SourceMixCycles: int
    SourceLiquidClassCategory: str
    DestinationLayoutItemInstance: CoverablePosition | NonCoverablePosition
    DestinationPosition: int  # This is the well position. Not sequence position
    CurrentDestinationVolume: float
    DestinationMixCycles: int
    DestinationLiquidClassCategory: str
    TransferVolume: float
