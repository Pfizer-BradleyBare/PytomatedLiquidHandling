from ....HAL.Layout import LayoutItem
from ....Tools.AbstractClasses import ObjectABC


class Sequence(ObjectABC):
    def __init__(
        self,
        Well: int,
        DestinationLayoutItemInstance: LayoutItem,
        SourceLayoutItemInstance: LayoutItem,
        AspirateMixCycles: int,
        DispenseMixCycles: int,
        TransferVolume: float,
    ):
        self.Well: int = Well

        self.DestinationLayoutItemInstance: LayoutItem = DestinationLayoutItemInstance
        self.SourceLayoutItemInstance: LayoutItem = SourceLayoutItemInstance

        self.AspirateMixCycles: int = AspirateMixCycles
        self.DispenseMixCycles: int = DispenseMixCycles

        self.TransferVolume: float = TransferVolume

    def GetName(self) -> int:
        return self.Well

    def GetDestinationLayoutItem(self) -> LayoutItem:
        return self.DestinationLayoutItemInstance

    def GetSourceLayoutItem(self) -> LayoutItem:
        return self.SourceLayoutItemInstance

    def GetAspirateMixCycles(self) -> int:
        return self.AspirateMixCycles

    def GetDispenseMixCycles(self) -> int:
        return self.DispenseMixCycles

    def GetTransferVolume(self) -> float:
        return self.TransferVolume
