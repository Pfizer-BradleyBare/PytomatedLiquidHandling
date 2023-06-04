from .....Tools.AbstractClasses import UniqueObjectABC
from ....Tip.BaseTip import Tip
from .LiquidClass.LiquidClassCategoryTracker import LiquidClassCategoryTracker


class PipetteTip(UniqueObjectABC):
    def __init__(
        self,
        TipInstance: Tip,
        LiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker,
        WasteSequence: str,
    ):
        UniqueObjectABC.__init__(self, self.TipInstance.GetUniqueIdentifier())
        self.TipInstance: Tip = TipInstance
        self.LiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker = (
            LiquidClassCategoryTrackerInstance
        )
        self.WasteSequence: str = WasteSequence
