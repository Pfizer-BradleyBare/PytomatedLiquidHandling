from ....Tools.AbstractClasses import ObjectABC
from ...Workbook.Block import BlockTracker
from .Well.WellTracker import WellTracker


class Container(ObjectABC):
    def __init__(self, Name: str, Filter: str):

        self.Name: str = Name

        # Block Instances: These are the blocks that have used this container.
        self.BlockTrackerInstance: BlockTracker = BlockTracker()

        # This is used for automated deck loading. We have to restrict the choices based on the filter
        self.Filter: str = Filter

        # What solutions and volume is in each well
        self.WellTrackerInstance: WellTracker = WellTracker()

    def GetName(self) -> str:
        return self.Name

    def GetBlockTracker(self) -> BlockTracker:
        return self.BlockTrackerInstance

    def GetFilter(self) -> str:
        return self.Filter

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance

    def GetMaxWellVolume(self) -> float:
        MaxVol = 0

        for WellInstance in self.WellTrackerInstance.GetObjectsAsList():
            if WellInstance.MaxWellVolume > MaxVol:
                MaxVol = WellInstance.MaxWellVolume

        return MaxVol

    def GetMinWellVolume(self) -> float:
        MinVol = 0

        for WellInstance in self.WellTrackerInstance.GetObjectsAsList():
            if WellInstance.MinWellVolume < MinVol:
                MinVol = WellInstance.MinWellVolume

        return MinVol
