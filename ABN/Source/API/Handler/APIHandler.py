from ...Tools.AbstractClasses import ServerHandlerABC
from .Endpoints import GetDevicesState, GetLoadedLabware
from ..Tools.LoadedLabwareConnection.LoadedLabware.LoadedLabwareTracker import (
    LoadedLabwareTracker,
)
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.HALLayer import HalLoader
from ..Tools.SymbolicSolution.SymbolicSolutionTracker import SymbolicSolutionTracker


class APIHandler(ServerHandlerABC):
    def __init__(self):
        self.SymbolicSolutionTrackerInstance: SymbolicSolutionTracker = (
            SymbolicSolutionTracker()
        )
        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()
        self.ResourceLockTrackerInstance: ResourceLockTracker = ResourceLockTracker()
        self.HALLayerInstance: HALLayer = HalLoader.Load()

    def GetName(self) -> str:
        return "API"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        pass
