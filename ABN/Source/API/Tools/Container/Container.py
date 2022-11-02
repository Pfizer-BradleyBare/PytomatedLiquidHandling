from ....AbstractClasses import ObjectABC
from ...Workbook.Block import BlockTracker
from .Well.WellTracker import WellTracker


class Container(ObjectABC):
    def __init__(self, Name: str, Filter: str | None):

        self.Name: str = Name

        # Block Instances: These are the blocks that have used this container. Either for aspirate or dispense.
        self.AspirateBlockTrackerInstance: BlockTracker = BlockTracker()
        self.DispenseBlockTrackerInstance: BlockTracker = BlockTracker()

        # This is used for automated deck loading. We have to restrict the choices based on the filter
        self.Filter: str | None = Filter

        # What solutions and volume is in each well
        self.WellTrackerInstance: WellTracker = WellTracker()

    def GetName(self) -> str:
        return self.Name

    def GetAspirateBlockTracker(self) -> BlockTracker:
        return self.AspirateBlockTrackerInstance

    def GetDispenseBlockTracker(self) -> BlockTracker:
        return self.DispenseBlockTrackerInstance

    def GetFilter(self) -> str | None:
        return self.Filter

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance
