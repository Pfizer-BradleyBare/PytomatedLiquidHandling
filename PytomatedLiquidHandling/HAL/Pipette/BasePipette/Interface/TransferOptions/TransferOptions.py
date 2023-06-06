from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(NonUniqueObjectABC):
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
