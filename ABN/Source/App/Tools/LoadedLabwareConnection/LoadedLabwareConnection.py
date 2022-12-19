from ....Tools.AbstractClasses import ObjectABC
from .LabwareSelection.LabwareSelection import LabwareSelection
from .LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker


class LoadedLabwareConnection(ObjectABC):
    def __init__(self, Name: str, LabwareSelectionInstance: LabwareSelection):
        self.Name: str = Name
        self.LabwareSelectionInstance: LabwareSelection = LabwareSelectionInstance
        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()

    def GetName(self) -> str:
        return self.Name

    def IsConnected(self):
        # Must contain at leat 1 lasbware to be considered as connected
        return self.LoadedLabwareTrackerInstance.GetNumObjects() != 0

    def GetLabwareSelection(self):
        return self.LabwareSelectionInstance

    def GetLoadedLabwareTracker(self) -> LoadedLabwareTracker:
        if self.IsConnected() is False:
            raise Exception(
                "There are no labware loaded in the tracker. Did you check IsConnected first?"
            )

        return self.LoadedLabwareTrackerInstance
