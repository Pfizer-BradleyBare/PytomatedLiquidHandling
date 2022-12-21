from ....HAL.Layout import LayoutItemGrouping
from ....Tools.AbstractClasses import ObjectABC
from .WellAssignment.BaseWellAssignment.WellAssignmentTracker import (
    WellAssignmentTracker,
)


class LoadedLabware(ObjectABC):
    Counter: int = 1

    def __init__(self, LayoutItemGroupingInstance: LayoutItemGrouping):
        self.Name: str = (
            LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance.GetName()
            + str(LoadedLabware.Counter)
        )
        LoadedLabware.Counter += 1

        self.LayoutItemGroupingInstance: LayoutItemGrouping = LayoutItemGroupingInstance

        self.WellAssignmentTrackerInstance = WellAssignmentTracker()

    def GetName(self) -> str:
        return self.Name

    def GetLayoutItemGrouping(self) -> LayoutItemGrouping:
        return self.LayoutItemGroupingInstance

    def GetWellAssignmentTracker(self) -> WellAssignmentTracker:
        return self.WellAssignmentTrackerInstance
