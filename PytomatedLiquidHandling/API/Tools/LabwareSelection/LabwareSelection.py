from ....HAL.Labware import Labware, LabwareTracker
from ....Tools.AbstractClasses import UniqueObjectABC
from ..Container.BaseContainer.Container import Container


class LabwareSelection(UniqueObjectABC):
    def __init__(self, ContainerInstance: Container):
        UniqueObjectABC.__init__(self, ContainerInstance.UniqueIdentifier)
        self.ContainerInstance: Container = ContainerInstance
        self.LabwareTrackerInstance: LabwareTracker = LabwareTracker()
        self.LabwareInstance: Labware | None = None

    def GetContainer(self) -> Container:
        return self.ContainerInstance

    def GetLabwareTracker(self) -> LabwareTracker:
        return self.LabwareTrackerInstance

    def GetLabware(self) -> Labware | None:
        return self.LabwareInstance
