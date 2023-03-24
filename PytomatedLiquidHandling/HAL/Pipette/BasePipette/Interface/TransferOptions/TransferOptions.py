from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Layout import LayoutItem


class TransferOptions(NonUniqueObjectABC):
    def __init__(
        self,
        SourceLayoutItemInstance: LayoutItem,
        SourcePosition: int,  # This is the well position. Not sequence position
        CurrentSourceVolume: float,
        SourceMixCycles: int,
        SourceLiquidClassCategory: str,
        DestinationLayoutItemInstance: LayoutItem,
        DestinationPosition: int,  # This is the well position. Not sequence position
        CurrentDestinationVolume: float,
        DestinationMixCycles: int,
        DestinationLiquidClassCategory: str,
        TransferVolume: float,
    ):
        self.SourceLayoutItemInstance: LayoutItem = SourceLayoutItemInstance
        self.SourcePosition: int = SourcePosition
        self.CurrentSourceVolume: float = CurrentSourceVolume
        self.SourceMixCycles: int = SourceMixCycles
        self.SourceLiquidClassCategory: str = SourceLiquidClassCategory

        self.DestinationLayoutItemInstance: LayoutItem = DestinationLayoutItemInstance
        self.DestinationPosition: int = DestinationPosition
        self.CurrentDestinationVolume: float = CurrentDestinationVolume
        self.DestinationMixCycles: int = DestinationMixCycles
        self.DestinationLiquidClassCategory: str = DestinationLiquidClassCategory

        self.TransferVolume: float = TransferVolume
        self.NumTransfers: int = 1
