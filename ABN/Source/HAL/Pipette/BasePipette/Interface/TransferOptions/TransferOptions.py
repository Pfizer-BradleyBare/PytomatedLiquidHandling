from ......Tools.AbstractClasses import ObjectABC
from .....Layout import LayoutItem


class TransferOptions(ObjectABC):
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
        DestinationLiquidCLassCategory: str,
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
        self.DestinationLiquidCLassCategory: str = DestinationLiquidCLassCategory

        self.TransferVolume: float = TransferVolume
