import os

from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools.HALLayer import HalLoader
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker
from .Endpoints import GetDevicesState, GetLoadedLabware


class APIHandler(ServerHandlerABC):
    def __init__(self):
        ServerHandlerABC.__init__(self)
        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()
        self.ResourceLockTrackerInstance: ResourceLockTracker = ResourceLockTracker()
        self.HALLayerInstance: HALLayer = HalLoader.Load(
            os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                ),
                "AutomationBareNecessitiesConfiguration",
                "HAL",
            )
        )

    def GetName(self) -> str:
        return "API"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        pass
