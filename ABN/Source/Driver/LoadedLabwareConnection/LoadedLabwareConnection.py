from ...Tools.AbstractClasses import ObjectABC
from ...API.Tools.Container import Container
from ...HAL.Tools import LoadedLabwareTracker
from ...HAL.Tools import LabwareSelection


class LoadedLabwareConnection(ObjectABC):
    def __init__(
        self, ContainerInstance: Container, LabwareSelectionInstance: LabwareSelection
    ):
        self.ContainerInstance: Container = ContainerInstance
        self.LabwareSelectionInstance: LabwareSelection = LabwareSelectionInstance
        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()

    def GetName(self) -> str:
        return self.ContainerInstance.GetName()

    def GetContainerInstance(self) -> Container:
        return self.ContainerInstance

    def IsConnected(self):
        return self.LoadedLabwareTrackerInstance.GetNumObjects() != 0

    def GetLabwareSelection(self):
        return self.LabwareSelectionInstance

    def GetLoadedLabwareTracker(self) -> LoadedLabwareTracker:
        if self.IsConnected() is False:
            raise Exception(
                "There are no labware loaded in the tracker. Did you check IsConnected first?"
            )

        return self.LoadedLabwareTrackerInstance
