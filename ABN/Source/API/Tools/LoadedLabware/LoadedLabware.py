from ....HAL.Layout import LayoutItem
from ....Tools.AbstractClasses import ObjectABC
from .WellAssignment.BaseWellAssignment.WellAssignmentTracker import (
    WellAssignmentTracker,
)


class LoadedLabware(ObjectABC):
    Counter: int = 1

    def __init__(self, LayoutItemInstance: LayoutItem):
        self.Name: str = LayoutItemInstance.LabwareInstance.GetName() + str(
            LoadedLabware.Counter
        )
        LoadedLabware.Counter += 1

        self.LayoutItemInstance: LayoutItem = LayoutItemInstance

        self.WellAssignmentTrackerInstance = WellAssignmentTracker()

    def GetName(self) -> str:
        return self.Name

    def GetLayoutItem(self) -> LayoutItem:
        return self.LayoutItemInstance

    def GetWellAssignmentTracker(self) -> WellAssignmentTracker:
        return self.WellAssignmentTrackerInstance
