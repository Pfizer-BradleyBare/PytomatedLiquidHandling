from ...Tools.AbstractClasses import ServerHandlerABC
from .Endpoints import GetDevicesState, GetLoadedLabware
from ..Tools.LoadedLabwareConnection.LoadedLabware.LoadedLabwareTracker import (
    LoadedLabwareTracker,
)


class APIHandler(ServerHandlerABC):
    def __init__(self):
        self.LoadedLabwareTrackerInstance: LoadedLabwareTracker = LoadedLabwareTracker()

    def GetName(self) -> str:
        return "Driver"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        pass
