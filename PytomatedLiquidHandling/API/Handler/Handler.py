from ...HAL.Handler import GetHandler as HALGetHandler
from ...HAL.Handler import Handler as HALHandler
from ...Tools.AbstractClasses import ServerHandlerABC
from ...Tools.Logger import Logger
from ..Tools.HALLayer import HalLoader
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


class Handler(ServerHandlerABC):
    def __init__(self, LoggerInstance: Logger, HALConfigurationFilesPath: str):
        ServerHandlerABC.__init__(self, LoggerInstance)

        global _HandlerInstance
        _HandlerInstance = self

        try:
            HALGetHandler()
        except:
            HALHandler(LoggerInstance)

        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()
        self.ResourceLockTrackerInstance: ResourceLockTracker = ResourceLockTracker()
        self.HALLayerInstance: HALLayer = HalLoader.Load(HALConfigurationFilesPath)

    def GetUniqueIdentifier(self) -> str:
        return "API"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        pass


_HandlerInstance: Handler | None = None


def GetHandler() -> Handler:
    if _HandlerInstance is None:
        raise Exception("Driver Handler not created. Please Create")

    else:
        return _HandlerInstance
