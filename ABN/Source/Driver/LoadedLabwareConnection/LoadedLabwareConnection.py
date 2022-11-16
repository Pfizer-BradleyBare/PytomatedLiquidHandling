from ...Tools.AbstractClasses import ObjectABC
from ...API.Tools.Container import Container
from ...HAL.Tools import LoadedLabware
from ...HAL.Tools import LabwareSelection


class LoadedLabwareConnection(ObjectABC):
    def __init__(
        self, ContainerInstance: Container, LabwareSelectionInstance: LabwareSelection
    ):
        self.ContainerInstance: Container = ContainerInstance
        self.LabwareSelectionInstance: LabwareSelection = LabwareSelectionInstance
        self.LoadedLabwareInstance: LoadedLabware | None = None

    def GetName(self) -> str:
        return self.ContainerInstance.GetName()

    def GetContainerInstance(self) -> Container:
        return self.ContainerInstance

    def IsConnected(self):
        return self.LoadedLabwareInstance is not None

    def GetLabwareSelection(self):
        return self.LabwareSelectionInstance

    def GetLoadedLabwareInstance(self) -> LoadedLabware:
        if self.LoadedLabwareInstance is None:
            raise Exception(
                "Loaded labware is none. Did you check if it is connected first?"
            )

        return self.LoadedLabwareInstance
