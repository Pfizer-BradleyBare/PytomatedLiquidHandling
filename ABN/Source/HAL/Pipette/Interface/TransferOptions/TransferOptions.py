from .....Tools.AbstractClasses import ObjectABC
from ....Layout import LayoutItem


class TransferOptions(ObjectABC):
    def __init__(
        self,
        SourceLayoutItemInstance: LayoutItem,
        SourcePosition: int,
        SourceVolume: float,  # Can be zero
        SourceMixCycles: int,
        SourceLiquidClass: str,
        DestinationLayoutItemInstance: LayoutItem,
        DestinationPosition: int,
        DestinationVolume: float,
        DestinationMixCycles: int,
        DestinationLiquidCLass: str,
        ReuseTips: bool,
        StoreTips: bool,
    ):
        self.SourceLayoutItemInstance: LayoutItem = SourceLayoutItemInstance
        self.SourcePosition: int = SourcePosition
        self.SourceVolume: float = SourceVolume  # if non-zero then fixed height will be used else LLD and if LLD fails then bottom
        self.SourceMixCycles: int = SourceMixCycles
        self.SourceLiquidClass: str = SourceLiquidClass

        self.DestinationLayoutItemInstance: LayoutItem = DestinationLayoutItemInstance
        self.DestinationPosition: int = DestinationPosition
        self.DestinationVolume: float = DestinationVolume
        self.DestinationMixCycles: int = DestinationMixCycles
        self.DestinationLiquidCLass: str = DestinationLiquidCLass

        self.ReuseTips: bool = ReuseTips
        self.StoreTips: bool = StoreTips
