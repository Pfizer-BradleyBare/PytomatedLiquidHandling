from .....Tools.AbstractClasses import UniqueObjectABC
from ....Tip.BaseTip import Tip
from .LiquidClass.LiquidClassCategoryTracker import LiquidClassCategoryTracker


class PipetteTip(UniqueObjectABC):
    def __init__(
        self,
        TipInstance: Tip,
        LiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker,
        ReusePickupSequence: str,
        ReuseDropoffSequence: str,
        WasteSequence: str,
    ):
        self.TipInstance: Tip = TipInstance
        self.LiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker = (
            LiquidClassCategoryTrackerInstance
        )
        self.ReusePickupSequence: str = ReusePickupSequence
        self.ReuseDropoffSequence: str = ReuseDropoffSequence
        self.WasteSequence: str = WasteSequence

    def GetName(self) -> str:
        return self.TipInstance.GetName()
