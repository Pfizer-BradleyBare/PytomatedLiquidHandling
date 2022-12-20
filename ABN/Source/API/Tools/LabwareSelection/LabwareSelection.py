from ....HAL.Labware import LabwareTracker
from ....Tools.AbstractClasses import ObjectABC


class LabwareSelection(ObjectABC):
    def __init__(self, Name: str):
        self.Name: str = Name
        self.LabwareTrackerInstance: LabwareTracker = LabwareTracker()

    def GetName(self) -> str:
        return self.Name

    def GetLabwareTracker(self) -> LabwareTracker:
        return self.LabwareTrackerInstance
