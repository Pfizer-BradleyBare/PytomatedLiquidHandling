from ....AbstractClasses import ObjectABC
from ...Workbook.Block import Block
from ...Workbook.Block import BlockTracker
from .Well.WellTracker import WellTracker


class Container(ObjectABC):
    def __init__(self, Name: str, Filter: str):

        self.Name: str = Name

        # Block Instances: These are the blocks that have used this container. Either for aspirate or dispense.
        self.AspirateBlockTrackerInstance: BlockTracker = BlockTracker()
        self.DispenseBlockTrackerInstances: BlockTracker = BlockTracker()

        # This is used for automated deck loading. We have to restrict the choices based on the filter
        self.Filter: str = Filter

        # What solutions and volume is in each well
        self.WellTrackerInstance: WellTracker = WellTracker()

        # What wells have been overaspirated
        self.WellOverAspirateTrackerInstance: WellTracker = WellTracker()

        self.MaxWellVolume: float = 0

    def GetName(self) -> str:
        return self.Name

    def GetAspirateBlocks(self) -> list[Block]:
        return self.AspirateBlockInstances

    def GetDispenseBlocks(self) -> list[Block]:
        return self.DispenseBlockInstances

    def GetFilter(self) -> str:
        return self.Filter

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance

    def GetWellOverAspirateTracker(self) -> WellTracker:
        return self.WellOverAspirateTrackerInstance

    def GetMaxVolume(self) -> float:
        return self.MaxWellVolume
