from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        SourceLayoutItemInstance: CoverablePosition | NonCoverablePosition,
        SourcePosition: int,  # This is the well position. Not sequence position
        CurrentSourceVolume: float,
        SourceMixCycles: int,
        SourceLiquidClassCategory: str,
        DestinationLayoutItemInstance: CoverablePosition | NonCoverablePosition,
        DestinationPosition: int,  # This is the well position. Not sequence position
        CurrentDestinationVolume: float,
        DestinationMixCycles: int,
        DestinationLiquidClassCategory: str,
        TransferVolume: float,
    ):
        self.SourceLayoutItemInstance: CoverablePosition | NonCoverablePosition = (
            SourceLayoutItemInstance
        )
        self.SourcePosition: int = SourcePosition
        self.CurrentSourceVolume: float = CurrentSourceVolume
        self.SourceMixCycles: int = SourceMixCycles
        self.SourceLiquidClassCategory: str = SourceLiquidClassCategory

        self.DestinationLayoutItemInstance: CoverablePosition | NonCoverablePosition = (
            DestinationLayoutItemInstance
        )
        self.DestinationPosition: int = DestinationPosition
        self.CurrentDestinationVolume: float = CurrentDestinationVolume
        self.DestinationMixCycles: int = DestinationMixCycles
        self.DestinationLiquidClassCategory: str = DestinationLiquidClassCategory

        self.TransferVolume: float = TransferVolume
        self.NumTransfers: int = 1
