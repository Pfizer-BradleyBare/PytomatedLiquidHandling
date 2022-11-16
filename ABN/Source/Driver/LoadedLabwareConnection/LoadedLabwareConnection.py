from ...Tools.AbstractClasses import ObjectABC
from ...API.Tools.Container import Container
from ...HAL.Tools import LoadedLabware


class LoadedLabwareConnection(ObjectABC):
    def __init__(
        self, ContainerInstance: Container, LoadedLabwareInstance: LoadedLabware
    ):
        self.ContainerInstance: Container = ContainerInstance
        self.LoadedLabwareInstance: LoadedLabware = LoadedLabwareInstance

    def GetName(self) -> str:
        return self.ContainerInstance.GetName()

    def GetContainerInstance(self) -> Container:
        return self.ContainerInstance

    def GetLoadedLabwareInstance(self) -> LoadedLabware:
        return self.LoadedLabwareInstance
