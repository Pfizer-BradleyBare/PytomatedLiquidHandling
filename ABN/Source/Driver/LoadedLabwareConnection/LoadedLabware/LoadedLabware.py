from ....HAL.Labware import Labware
from ....HAL.Layout import LayoutItem
from ....Tools.AbstractClasses import ObjectABC
from .WellAssignment.WellAssignmentTracker import WellAssignmentTracker


class LoadedLabware(ObjectABC):
    Counter: int = 1

    def __init__(self, LabwareInstance: Labware, LayoutItemInstance: LayoutItem):
        self.Name: str = LabwareInstance.GetName() + str(LoadedLabware.Counter)
        LoadedLabware.Counter += 1

        self.LabwareInstance: Labware = LabwareInstance
        self.LayoutItemInstance: LayoutItem = LayoutItemInstance

        self.WellAssignmentTrackerInstance = WellAssignmentTracker()

    def GetName(self) -> str:
        return self.Name

    def GetLabware(self) -> Labware:
        return self.LabwareInstance

    def GetLayoutItem(self) -> LayoutItem:
        return self.LayoutItemInstance

    def GetWellAssignmentTracker(self) -> WellAssignmentTracker:
        return self.WellAssignmentTrackerInstance
