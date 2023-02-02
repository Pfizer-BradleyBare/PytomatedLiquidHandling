from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools.HALLayer import HalLoader
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


class Handler(ServerHandlerABC):
    def __init__(self, HALConfigurationFilesPath: str):
        ServerHandlerABC.__init__(self)
        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()
        self.ResourceLockTrackerInstance: ResourceLockTracker = ResourceLockTracker()
        self.HALLayerInstance: HALLayer = HalLoader.Load(HALConfigurationFilesPath)

    def GetName(self) -> str:
        return "API"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        pass
