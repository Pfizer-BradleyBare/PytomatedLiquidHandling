from ....HAL.Labware import Labware, LabwareTracker
from ....Tools.AbstractClasses import ObjectABC
from ..Container.BaseContainer.Container import Container


class LabwareSelection(ObjectABC):
    def __init__(self, ContainerInstance: Container):
        self.ContainerInstance: Container = ContainerInstance
        self.LabwareTrackerInstance: LabwareTracker = LabwareTracker()
        self.LabwareInstance: Labware | None = None

    def GetName(self) -> str:
        return self.ContainerInstance.GetName()

    def GetContainer(self) -> Container:
        return self.ContainerInstance

    def GetLabwareTracker(self) -> LabwareTracker:
        return self.LabwareTrackerInstance

    def GetLabware(self) -> Labware | None:
        return self.LabwareInstance
